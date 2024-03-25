import datetime
import json
import traceback
from abc import ABC, abstractmethod
from typing import List, Callable, Any, Union, Dict, Tuple

import rdflib
from wzl.mqtt.client import MQTTPublisher
from wzl.mqtt.exceptions import ClientNotFoundError

from . import variable
from .component import Component
from .event import Event
from .semantics import Namespaces
from ..utils import root_logger
from ..utils import serialize
from ..utils.resources import ResourceType

logger = root_logger.get(__name__)


class JobError(Exception):

    def __init__(self, message: str, predeccessor: Exception = None):
        self._predecessor: predeccessor
        self._message = message

    @property
    def message(self) -> str:
         return self._message




class Job(ABC):
    """Abstract base class for all jobs containing the basic information for continuous automatic data streaming.

    Attributes:
        topic: The topic to which a message should be published, if the job is triggered.
        callback: Method to be called if the job is triggered to retrieve the value to be published.
        next: Point in time (future) at which the job has to be checked again.

    """

    def __init__(self, topic: str, callback: Callable):
        """Constructor

        Args:
            topic: The topic as used in a publish/subscribe-protocol under the which the data is published.
            callback: A method called if the job is triggered to retrieve the value to be published.
            next: Point in time (future) at which the job has to be checked again.
        """
        self._topic = topic
        self._callback = callback
        self._next = datetime.datetime.now()

    @property
    def type(self) -> str:
        return 'measurement'

    @property
    def topic(self) -> str:
        return self._topic

    @property
    @abstractmethod
    def interval(self) -> float:
        ...

    @property
    def value(self) -> Tuple[Any, Any]:
        """

        Returns: the value together with the covariance, which might None

        """
        return self._callback()

    def is_triggered(self, time: datetime.datetime = None) -> bool:
        try:
            time = time if time is not None else datetime.datetime.now()
            return self._next is not None and self._next <= time and self._is_triggered()
        except Exception as e:
            raise JobError('is_triggered failed', predeccessor=e)

    @abstractmethod
    def _is_triggered(self) -> bool:
        ...

    def determine_next(self, time: datetime.datetime) -> datetime.datetime:
        if time is None or (self._next is not None and self._next < time):
            return self._next
        else:
            return time

    def start(self) -> None:
        self._next = datetime.datetime.now() + datetime.timedelta(seconds=self.interval)

    def schedule(self) -> None:
        if self._next is not None:
            self.start()

    def stop(self) -> None:
        self._next = None

    def data(self, model: Component = None) -> Dict:
        if model is None:
            raise JobError('Can not retrieve data. Model is missing')
        try:
            uuids = self.topic.split('/')
            data = model.__getitem__(uuids).serialize([], False)

            value, covariance = self.value
            data['uuid'] = self.topic
            data['value'] = value
            data['covariance'] = covariance
            data['timestamp'] = variable.serialize_time(datetime.datetime.now())
            return data
        except Exception as e:
            raise JobError('Can not retrieve data. Due to another error.', predeccessor=e)

    def semantic_data(self, model: Component = None) -> (str, rdflib.Graph):
        if model is None:
            raise JobError('Can not retrieve semantic data. Model is missing')
        try:
            uuids = self.topic.split('/')
            element = model.__getitem__(uuids)
            data = element.serialize_semantics(ResourceType.data)
            data += element.serialize_semantics(ResourceType.uncertainty)
            data += element.serialize_semantics(ResourceType.observation)

            measurement_subject = \
                list((data.subjects(predicate=Namespaces.rdf.type, object=Namespaces.sosa.Observation)))[0]

            # replace value
            data.remove((None, Namespaces.qudt.value, None))
            value, covariance = self.value
            data.add((measurement_subject, Namespaces.qudt.value, element.serialize_value(data, value)))

            # replace timestamp
            data.remove((None, Namespaces.schema.dateCreated, None))
            data.add((measurement_subject, Namespaces.schema.dateCreated, rdflib.Literal(datetime.datetime.now())))

            return element.semantic_name, data
        except Exception as e:
            raise JobError('Can not semantic retrieve data. Due to another error.', predeccessor=e)


class FixedJob(Job):

    def __init__(self, topic: str, interval: float, callback: Callable):
        Job.__init__(self, topic, callback)
        self._interval = interval
        self.schedule()

    @property
    def interval(self) -> float:
        return self._interval

    def _is_triggered(self) -> bool:
        return True


class ConfigurableJob(Job):
    """
    Works exactly as a Job, despite interval is a callable which returns an integer value, used for determining delay between two job executions.
    """

    def __init__(self, topic: str, interval: Callable, callback: Callable):
        Job.__init__(self, topic, callback)
        self._interval = interval
        self.schedule()

    @property
    def interval(self) -> Union[int, float]:
        return self._interval()

    def _is_triggered(self) -> bool:
        return True


class UpdateJob(FixedJob):

    def __init__(self, topic: str, callback: Callable):
        FixedJob.__init__(self, topic, 0.01, callback)
        self._last_value = None
        self._last_covariance = None

    def _is_triggered(self) -> bool:
        value, covariance = self._callback()
        updated = self._last_value != value
        self._last_value = value
        self._last_covariance = covariance
        if isinstance(updated, list):
            updated = any(updated)
        return updated

    @property
    def value(self) -> Tuple[Any, Any]:
        return self._last_value, self._last_covariance


class EventJob(FixedJob):

    def __init__(self, topic: str, interval: int, callback: Callable, event: Event):
        FixedJob.__init__(self, f'events/{topic}', interval, callback)
        self._event = event
        self._last_value = None

    @property
    def type(self) -> str:
        return 'event'

    def _is_triggered(self) -> bool:
        value = self._callback()
        if isinstance(value, tuple):
            assert len(value) == 2
            value, covariance = value

        updated = self._event.is_triggered(value)
        if isinstance(updated, list):
            updated = any(updated)
        return updated

    def data(self, model: Dict = None) -> Dict:
        self._event.trigger(self._last_value)
        return self._event.serialize()


class StreamScheduler(object):
    """Processes Jobs and published messages if, certain conditions are met.

    Periodically, checks the status of scheduled jobs. If a job is triggered, it publishes a message via all publishers handed to the scheduler.
    """

    def __init__(self, loop, schedule: List[Job], publisher: MQTTPublisher = None,
                 start_immediately: bool = False, dataformat: str = 'json', model: 'Component' = None):
        """Constructor.

        Args:
            loop:
            schedule: List of jobs scheduled be checked regularly.
            publishers: List of MQTT publishers, which are used to publish a message if a job is triggered.
            start_immediately: If True, the all jobs are scheduled immediately, i.e. the update method is called checking the jobs.
        """
        if dataformat not in ['json', 'xml']:
            raise ValueError('Dataformat must be one of "json" or "xml".')

        self._loop = loop
        self._schedule: List[Job] = schedule
        self._publisher: MQTTPublisher = publisher if publisher is not None else []
        self._running: bool = start_immediately
        self._dataformat: str = dataformat
        self._model: Component = model
        if start_immediately:
            self._update()

    def start(self) -> None:
        """Schedules all jobs stored in the attribute _schedule.

        """
        self._running = True
        self._update()

    def stop(self) -> None:
        """Stops scheduling and processing of jobs.

        """
        self._running = False

    def add_jobs(self, schedule: List[Job]):
        self._schedule += schedule

    def remove_jobs(self, fqid: str):
        jobs_to_remove = []
        for job in self._schedule:
            if fqid in job.topic:
                jobs_to_remove += [jobs_to_remove]
        for job in jobs_to_remove:
            self._schedule.remove(job)

    def _update(self) -> None:
        """Processes all scheduled jobs.

        Method calls itself infinitely, until stop() is called.
        Checks for all jobs, if it is triggered, and publishes messages, if triggered.
        Computes the interval to the next due job, and schedules the call of _update accordingly.

        Returns:

        """
        if self._running:
            next = None
            now = datetime.datetime.now()
            for job in self._schedule:
                try:
                    if job.is_triggered(now):
                        # send syntactic data package
                        if self._dataformat == 'json':
                            message = json.dumps(job.data(self._model))
                        elif self._dataformat == 'xml':
                            message = serialize.to_xml(job.type, job.data(self._model))

                        try:
                            self._publisher.get('tier1').publish(job.topic, message, 1)
                        except ClientNotFoundError:
                            logger.warn('Client not found error occured.')
                            logger.warn(traceback.format_exc())
                            self._publisher.publish(job.topic, message, 1)

                        # try to send semantic data package
                        try:
                            url, semantic_data = job.semantic_data(self._model)
                            url = url.replace('https://', '').replace('http://', '')
                            if self._dataformat == 'json':
                                message = semantic_data.serialize(format='json-ld')
                            elif self._dataformat == 'xml':
                                message = semantic_data.serialize(format='xml')

                            try:
                                self._publisher.get('tier2').publish(url, message, 1)
                            except ClientNotFoundError:
                                logger.warn('Client not found error occured.')
                                logger.warn(traceback.format_exc())
                                self._publisher.publish(url, message, 1)

                        except JobError as e:
                            logger.error(e.message)
                            logger.error(traceback.format_exc())

                    job.schedule()
                    next = job.determine_next(next)
                except JobError as e:
                    logger.error(e.message)
                    logger.error(traceback.format_exc())
                    pass

            if next is None:
                next = now + datetime.timedelta(seconds=10)
            elif next < now:
                next = now

            self._loop.call_later((next - now).seconds + (next - now).microseconds / 1e6, self._update)
