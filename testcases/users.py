#!/usr/bin/python3

from testcases import Testcase, MonolithicTestcase
import logging


class UsersCreateFailed(Testcase):

    def test_partially_filled(self):
        fn = "test_partially_filled"
        logging.info('{} started'.format(fn))
        req_body = {
            'name': self.test_data['name'],
            'gender': self.test_data['gender']
        }
        req_headers = {
            'Authorization': 'Bearer {}'.format(self.app.access_token)
        }
        resp_json = self.app.request('/public-api/users', 'POST', req_headers=req_headers, req_body=req_body)
        operation_code_resp = resp_json['code']
        self.assertEqual(422, operation_code_resp)
        data_length = len(resp_json['data'])
        self.assertEqual(2, data_length)
        data = resp_json['data']
        for d in data:
            self.assertIn(d['field'], ['email', 'status'])
            self.assertEqual(d['message'], "can't be blank")
        logging.info('{} finished'.format(fn))

    def test_without_data(self):
        fn = "test_without_data"
        logging.info('{} started'.format(fn))
        req_headers = {
            'Authorization': 'Bearer {}'.format(self.app.access_token)
        }
        resp_json = self.app.request('/public-api/users', 'POST', req_headers=req_headers)
        operation_code_resp = resp_json['code']
        self.assertEqual(422, operation_code_resp)
        data_length = len(resp_json['data'])
        self.assertEqual(4, data_length)
        data = resp_json['data']
        for d in data:
            self.assertIn(d['field'], ['name', 'email', 'gender', 'status'])
            self.assertEqual(d['message'], "can't be blank")
        logging.info('{} finished'.format(fn))


class UsersCreatePassed(Testcase):

    def test_with_full_data(self):
        fn = "test_with_full_data"
        logging.info('{} started'.format(fn))
        req_body = {
            'name': self.test_data['name'],
            'gender': self.test_data['gender'],
            'email': self.test_data['email'],
            'status': self.test_data['status']
        }
        req_headers = {
            'Authorization': 'Bearer {}'.format(self.app.access_token)
        }
        resp_json = self.app.request('/public-api/users', 'POST', req_headers=req_headers, req_body=req_body)
        operation_code_resp = resp_json['code']
        self.assertEqual(201, operation_code_resp)
        data = resp_json['data']
        for k in req_body.keys():
            self.assertEqual(req_body[k], data[k])
        for k in ['id', 'created_at', 'updated_at']:
            self.assertNotEqual(data.get(k, None), None)
        print(data['id'])
        self.user_id = data['id']
        logging.info('{} finished'.format(fn))

    def tearDown(self) -> None:
        try:
            req_headers = {
                'Authorization': 'Bearer {}'.format(self.app.access_token)
            }
            self.app.request('/public-api/users/{}'.format(self.user_id), 'DELETE', req_headers=req_headers)
        except AttributeError:
            logging.warning('User Id is not present. Could not delete user')


class UsersReadPassed(Testcase):

    def setUp(self) -> None:
        logging.info('setUp started')
        req_body = {
            'name': self.test_data['name'],
            'gender': self.test_data['gender'],
            'email': self.test_data['email'],
            'status': self.test_data['status']
        }
        req_headers = {
            'Authorization': 'Bearer {}'.format(self.app.access_token)
        }
        resp_json = self.app.request('/public-api/users', 'POST', req_headers=req_headers, req_body=req_body)
        self.user_data = req_body
        self.user_data['id'] = resp_json['data']['id']
        logging.info('setUp finished')

    def test_read_by_id(self):
        fn = "test_read_by_id"
        logging.info('{} started'.format(fn))
        req_headers = {
            'Authorization': 'Bearer {}'.format(self.app.access_token)
        }
        resp_json = self.app.request('/public-api/users/{}'.format(self.user_data['id']), 'GET', req_headers=req_headers)
        operation_code_resp = resp_json['code']
        self.assertEqual(200, operation_code_resp)
        data = resp_json['data']
        for k in self.user_data.keys():
            self.assertEqual(self.user_data[k], data[k])
        for k in ['created_at', 'updated_at']:
            self.assertNotEqual(data.get(k, None), None)
        logging.info('{} started'.format(fn))

    def tearDown(self) -> None:
        fn = "tearDown"
        logging.info('{} started'.format(fn))
        try:
            req_headers = {
                'Authorization': 'Bearer {}'.format(self.app.access_token)
            }
            self.app.request('/public-api/users/{}'.format(self.user_id), 'DELETE', req_headers=req_headers)
        except AttributeError:
            logging.warning('User Id is not present')


class UserTests(MonolithicTestcase):

    def step1_create_user_ok(self):
        fn = "step1_create_user_ok"
        logging.info('{} started'.format(fn))
        req_body = {
            'name': self.test_data['name'],
            'gender': self.test_data['gender'],
            'email': self.test_data['email'],
            'status': self.test_data['status']
        }
        req_headers = {
            'Authorization': 'Bearer {}'.format(self.app.access_token)
        }
        resp_json = self.app.request('/public-api/users', 'POST', req_headers=req_headers, req_body=req_body)
        operation_code_resp = resp_json['code']
        self.assertEqual(201, operation_code_resp)
        data = resp_json['data']
        for k in req_body.keys():
            self.assertEqual(req_body[k], data[k])
        for k in ['id', 'created_at', 'updated_at']:
            self.assertNotEqual(data.get(k, None), None)
        self.user_data = req_body
        self.user_data['id'] = data['id']
        logging.info('{} finished'.format(fn))

    def step2_read_user_ok(self):
        fn = "step2_read_user_ok"
        logging.info('{} started'.format(fn))
        req_headers = {
            'Authorization': 'Bearer {}'.format(self.app.access_token)
        }
        resp_json = self.app.request('/public-api/users/{}'.format(self.user_data['id']), 'GET',
                                     req_headers=req_headers)
        operation_code_resp = resp_json['code']
        self.assertEqual(200, operation_code_resp)
        data = resp_json['data']
        for k in self.user_data.keys():
            self.assertEqual(self.user_data[k], data[k])
        for k in ['created_at', 'updated_at']:
            self.assertNotEqual(data.get(k, None), None)
        logging.info('{} finished'.format(fn))

    def step3_delete_user_ok(self):
        fn = "step3_delete_user_ok"
        logging.info('{} started'.format(fn))
        req_headers = {
            'Authorization': 'Bearer {}'.format(self.app.access_token)
        }
        resp_json = self.app.request('/public-api/users/{}'.format(self.user_data['id']), 'DELETE', req_headers=req_headers)
        operation_code_resp = resp_json['code']
        self.assertEqual(204, operation_code_resp)
        self.assertEqual(resp_json['meta'], None)
        self.assertEqual(resp_json['data'], None)
        logging.info('{} finished'.format(fn))

    def step4_delete_user_failed(self):
        fn = "step4_delete_user_failed"
        logging.info('{} started'.format(fn))
        req_headers = {
            'Authorization': 'Bearer {}'.format(self.app.access_token)
        }
        resp_json = self.app.request('/public-api/users/{}'.format(self.user_data['id']), 'DELETE',
                                     req_headers=req_headers)
        operation_code_resp = resp_json['code']
        self.assertEqual(404, operation_code_resp)
        self.assertEqual(resp_json['meta'], None)
        self.assertEqual(resp_json['data']['message'], 'Resource not found')
        logging.info('{} started'.format(fn))