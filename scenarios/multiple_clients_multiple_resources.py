# -*- coding: utf-8 -*-
"""
Experiment scenario 2
Server unresponsive when multiple clients access different resource

Endpoints (shared between the requests):
* /user/#/signin
* /facility/#/classes
* /learn/#/topics/{id} : video
* /learn/#/topics/{id} : pdf
* /learn/#/topics/{id} : JavaScript (Phet or similars)
* … exercises, exams, coach pages


Channels    Learners        Classrooms     Requests/s   Database
================================================================
No              25              2           20          sqlite
large           25              2           20          sqlite
video           25              2           20          sqlite
video           25              2           100         sqlite
video           25              2           100         postgresql
Multiple        25              2           20          sqlite
Multiple        25              2           100         sqlite
Multiple        25              2           100         postgresql
"""
from __future__ import print_function, unicode_literals
import os
from locust import HttpLocust, task


try:
    from locust_user import KolibriUserBehavior, AdminUser
    from locust_wrapper import launch
except ImportError:
    # the test is being run out of velox environment
    # and velox package is not installed
    import sys
    sys.path.append(os.path.join(os.getcwd(), 'src'))
    from locust_user import KolibriUserBehavior, AdminUser
    from locust_wrapper import launch

admin = AdminUser(base_url=os.environ.get('KOLIBRI_BASE_URL', 'http://127.0.0.1:8000'))
KolibriUserBehavior.KOLIBRI_USERS = admin.get_users()
KolibriUserBehavior.KOLIBRI_RESOURCES = admin.get_resources()


class UserBehavior(KolibriUserBehavior):

    @task(40)
    def load_video_resources(self):
        self.load_resource('video')

    @task(50)
    def load_html5_resources(self):
        self.load_resource('html5')

    @task(20)
    def load_document_resources(self):
        self.load_resource('document')

    @task(30)
    def load_exercise_resources(self):
        self.load_resource('exercise')


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    # don't wait, hit the server as fast as you can:
    min_wait = 0
    max_wait = 0


def run(learners=30):
    rate = 40
    launch(WebsiteUser, learners, rate, run_time=120)


if __name__ == '__main__':
    run()
