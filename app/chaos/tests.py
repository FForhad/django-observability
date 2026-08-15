from django.test import TestCase, Client
from django.urls import reverse


class ObservabilityMetricsTests(TestCase):
    """Test suite for Prometheus metrics scraping endpoints."""

    def setUp(self):
        self.client = Client()

    def test_metrics_endpoint_returns_200(self):
        """Ensure /metrics endpoint is accessible and returns 200 OK."""
        response = self.client.get('/metrics')
        self.assertEqual(response.status_code, 200)

    def test_metrics_content_format(self):
        """Ensure /metrics contains standard Prometheus metric formatting."""
        response = self.client.get('/metrics')
        content = response.content.decode('utf-8')
        
        # Prometheus format assertions
        self.assertIn('# HELP', content)
        self.assertIn('# TYPE', content)
        self.assertIn('django_http', content)


class ChaosEndpointsTests(TestCase):
    """Test suite for chaos engineering simulation endpoints."""

    def setUp(self):
        self.client = Client()

    def test_chaos_index(self):
        """Ensure the chaos directory index lists all available endpoints."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'online')
        self.assertIn('endpoints', data)
        self.assertIn('health', data['endpoints'])
        self.assertIn('delay', data['endpoints'])
        self.assertIn('error', data['endpoints'])
        self.assertIn('cpu_spike', data['endpoints'])
        self.assertIn('memory_spike', data['endpoints'])
        self.assertIn('logs', data['endpoints'])

    def test_chaos_health_check(self):
        """Ensure health check returns 200 and healthy status."""
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'healthy')
        self.assertIn('timestamp', data)

    def test_chaos_delay(self):
        """Ensure delay endpoint processes duration parameter successfully."""
        response = self.client.get(reverse('delay'), {'seconds': 0.05})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertEqual(data.get('delay_seconds'), 0.05)

    def test_chaos_error_500(self):
        """Ensure error endpoint returns HTTP 500 status code."""
        response = self.client.get(reverse('error'), {'code': '500'})
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertEqual(data.get('code'), 500)

    def test_chaos_error_exception(self):
        """Ensure unhandled exception simulation raises an Exception."""
        with self.assertRaises(Exception):
            self.client.get(reverse('error'), {'code': 'exception'})

    def test_chaos_cpu_spike(self):
        """Ensure CPU spike endpoint performs computation and returns metrics."""
        response = self.client.get(reverse('cpu_spike'), {'duration': 0.05})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('duration_seconds', data)
        self.assertIn('operations', data)
        self.assertGreater(data.get('operations', 0), 0)

    def test_chaos_memory_spike(self):
        """Ensure memory spike endpoint allocates and frees memory cleanly."""
        response = self.client.get(reverse('memory_spike'), {'mb': 5})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'success')
        self.assertIn('size_mb', data)
        self.assertEqual(data.get('size_mb'), 5.0)

    def test_chaos_logs_various_levels(self):
        """Ensure logs endpoint handles different log levels without error."""
        for level in ['debug', 'info', 'warning', 'error', 'critical', 'all']:
            with self.subTest(level=level):
                response = self.client.get(reverse('logs'), {'level': level})
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertEqual(data.get('status'), 'success')
