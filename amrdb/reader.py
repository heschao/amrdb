from craniutil.dbtest.testdb import TestDb
import json
import os
import re
import subprocess
import traceback
from abc import ABCMeta, abstractmethod
from datetime import datetime
from time import sleep

import click
from sqlalchemy import create_engine, func, distinct

from amrdb.model import Base, Message, get_session

DEFAULT_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}).+Z')


def parse_timestamp(s, p=DEFAULT_PATTERN):
    m = p.search(s)
    return datetime.strptime(m.groups()[0], '%Y-%m-%dT%H:%M:%S.%f')


class Store:
    __metaclass__ = ABCMeta

    @abstractmethod
    def put(self, message):
        pass


class DbStore(Store):
    def __init__(self, session):
        self.session = session

    def put(self, message):
        self.session.add(message)
        self.session.commit()


class MemStore(Store):
    def __init__(self):
        self.x = {}

    def put(self, message):
        self.x[message.timestamp] = message


def get_store():
    return DbStore(get_session())


@click.group()
def main():
    pass


@main.command(name='create-tables')
def create_tables():
    connection_string = os.getenv('CONNECTION_STRING')
    assert connection_string, "connection string undefined"
    engine = create_engine(connection_string)
    click.echo('create tables...')
    Base.metadata.create_all(bind=engine, checkfirst=True)
    click.echo('done')


@main.command(name='status')
def status():
    session = get_session()
    c = session.query(Message).count()
    print('{} message recorded'.format(c))
    d = session.query(func.count(distinct(Message.device_id))).scalar()
    print('{} distinct device ids'.format(d))
    x = session.query(
        func.min(Message.timestamp).label('min'),
        func.max(Message.timestamp).label('max'),
    ).first()
    print('timetamps {} --> {}'.format(x.min, x.max))


@main.command(name='read')
@click.option('--rtl-host-port', '-h', default=os.getenv('RTL_TCP_HOST_PORT'))
@click.option('--verbose', '-v', is_flag=True)
@click.option('--max-errors', '-m', default=100)
@click.option('--test', '-t', is_flag=True)
def read(rtl_host_port, verbose, max_errors, test):
    assert rtl_host_port, "rtl_tcp host and port undefined"
    store = get_store()
    proc = get_fake_process() if test else get_process(rtl_host_port)
    read_until_errors(max_errors=max_errors, proc=proc, store=store, verbose=verbose)


def read_until_errors(proc, store, max_errors=100, verbose=False):
    n_errors = 0
    while n_errors < max_errors:
        line = proc.stdout.readline()
        if not isinstance(line,str):
            line = line.decode()
        try:
            if line != '':
                x = json.loads(line)
                msg = Message(
                    timestamp=parse_timestamp(x['Time']),
                    device_id=x['Message']['ID'],
                    device_type=x['Message']['Type'],
                    consumption=x['Message']['Consumption'],
                )
                if verbose:
                    print(msg)
                store.put(msg)
            else:
                break
        except Exception as e:
            n_errors += 1
            traceback.print_exc()
            print('line={}'.format(line))
            print('{} errors so far'.format(n_errors))

    if n_errors >= max_errors:
        print('max errors {} exceeded! Quit.'.format(max_errors))


class Test(TestDb):
    @classmethod
    def base(cls):
        return Base

    def test_read_until_end(self):
        try:
            store = DbStore(session=self.session)
            proc = get_fake_process(n=2)
            read_until_errors(max_errors=1, proc=proc, store=store, verbose=True)
            c = self.session.query(Message).count()
            assert c==2, c
        finally:
            self.session.query(Message).delete()


    def test_read_until_errors(self):
        try:
            store = DbStore(session=self.session)
            proc = get_error_process(n=2)
            read_until_errors(max_errors=1, proc=proc, store=store, verbose=True)
            c = self.session.query(Message).count()
            assert c==0, c
        finally:
            self.session.rollback()




@main.command(name='fake')
@click.option('--n','-n',default=10)
def fake(n):
    consumption = 100000
    for i in range(n):
        sleep(0.5)
        consumption += 1
        t = datetime.utcnow()
        s = json.dumps(dict(Time=t.strftime('%Y-%m-%dT%H:%M:%S.%f' + '.000Z'),
                                Message=dict(ID='12345', Type='4', Consumption=consumption)))
        print(s)


@main.command(name='error')
@click.option('--n','-n',default=10)
def error(n):
    consumption = 100000
    for i in range(n):
        sleep(0.5)
        consumption += 1
        t = datetime.utcnow()
        s = json.dumps(dict(Time=t.strftime('%Y-%m-%dT%H:%M:%S' + 'haha'),
                                Message=dict(ID='12345', Type='4', Consumption=consumption)))
        print(s)


def get_process(rtl_host_port):
    proc = subprocess.Popen(['rtlamr', '-server={}'.format(rtl_host_port), '-filtertype=4,7,12', '-format=json'],
                            stdout=subprocess.PIPE)
    return proc


def get_fake_process(n=10):
    proc = subprocess.Popen(['python3', '-u', 'amrdb/reader.py', 'fake', '-n', str(n)], stdout=subprocess.PIPE)
    return proc


def get_error_process(n=10):
    proc = subprocess.Popen(['python3', '-u', 'amrdb/reader.py', 'error', '-n', str(n)], stdout=subprocess.PIPE)
    return proc


if __name__ == "__main__":
    main()
