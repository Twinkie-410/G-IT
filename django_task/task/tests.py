from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from task.models import Task


class TaskTest(TestCase):
    tasks = [Task(tittle='task 1', description='its task 1', completed=True),
             Task(tittle='task 2', description='wow, its task 2', completed=False),
             Task(tittle='task 3', description='hehe, its task 3', completed=True)]

    def setUp(self):
        Task.objects.bulk_create(self.tasks)

    def test_create(self):
        data = {'tittle': 'test task',
                'description': 'its description for test task',
                'completed': True}
        response = self.client.post(reverse_lazy('task-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.get(id=response.data['id']))

        task = Task.objects.get(id=response.data['id'])
        self.assertEqual(task.tittle, data['tittle'])
        self.assertEqual(task.description, data['description'])
        self.assertEqual(task.completed, data['completed'])

    def test_create_without_optional_fields(self):
        data = {'tittle': 'test task'}
        response = self.client.post(reverse_lazy('task-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.get(id=response.data['id']))

        task = Task.objects.get(id=response.data['id'])
        self.assertEqual(task.tittle, data['tittle'])
        self.assertFalse(task.description)
        self.assertFalse(task.completed)

    def test_create_without_title(self):
        data = {'description': 'its description for test task',
                'completed': True}
        response = self.client.post(reverse_lazy('task-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_list(self):
        response = self.client.get(reverse_lazy('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_count = Task.objects.all().count()
        self.assertEqual(len(response.data), task_count)

    def test_get_by_id(self):
        task = self.tasks[0]
        response = self.client.get(reverse_lazy('task-detail', kwargs={'id': task.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.tittle, task.tittle)
        self.assertEqual(task.description, task.description)
        self.assertEqual(task.completed, task.completed)

    def test_get_by_non_exist_id(self):
        response = self.client.get(reverse_lazy('task-detail', kwargs={'id': len(self.tasks) + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch(self):
        task_1, task_2 = self.tasks[0], self.tasks[1]
        data_1, data_2 = {'tittle': 'it has changed'}, {'description': 'I have changed that'}

        response_1 = self.client.patch(reverse_lazy('task-detail', kwargs={'id': task_1.id}),
                                       data_1,
                                       format='json',
                                       content_type='application/json')
        task_1 = Task.objects.get(id=task_1.id)
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(task_1.tittle, data_1['tittle'])
        self.assertEqual(task_1.description, task_1.description)
        self.assertEqual(task_1.completed, task_1.completed)

        response_2 = self.client.patch(reverse_lazy('task-detail', kwargs={'id': task_2.id}),
                                       data_2,
                                       format='json',
                                       content_type='application/json')
        task_2 = Task.objects.get(id=task_2.id)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(task_2.tittle, task_2.tittle)
        self.assertEqual(task_2.description, data_2['description'])
        self.assertEqual(task_2.completed, task_2.completed)

    def test_put(self):
        task = self.tasks[0]
        data = {'tittle': 'changed tittle',
                'description': 'changed description',
                'completed': False}
        response = self.client.put(reverse_lazy('task-detail', kwargs={'id': task.id}),
                                   data,
                                   format='json',
                                   content_type='application/json')
        task = Task.objects.get(id=task.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.tittle, data['tittle'])
        self.assertEqual(task.description, data['description'])
        self.assertEqual(task.completed, data['completed'])

    def test_put_aborted(self):
        task = self.tasks[0]
        data = {'description': 'changed description'}
        response = self.client.put(reverse_lazy('task-detail', kwargs={'id': task.id}),
                                   data,
                                   format='json',
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        task = self.tasks[0]
        response = self.client.delete(reverse_lazy('task-detail', kwargs={'id': task.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=task.id)
