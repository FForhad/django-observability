import logging
import math
import time
from django.http import JsonResponse, HttpResponseServerError

logger = logging.getLogger('chaos')


def index(request):
    """List available chaos testing endpoints."""
    logger.info("Chaos index endpoint accessed.")
    return JsonResponse({
        "status": "online",
        "description": "Django Observability Chaos API",
        "endpoints": {
            "health": "/chaos/health/",
            "delay": "/chaos/delay/?seconds=2",
            "error": "/chaos/error/?code=500",
            "cpu_spike": "/chaos/cpu/?duration=2",
            "memory_spike": "/chaos/memory/?mb=50",
            "logs": "/chaos/logs/?level=error",
            "metrics": "/metrics",
        }
    })


def health_view(request):
    """Health check endpoint."""
    logger.debug("Health check invoked.")
    return JsonResponse({"status": "healthy", "timestamp": time.time()})


def delay_view(request):
    """Simulate latency and slow responses."""
    try:
        seconds = float(request.GET.get('seconds', 2))
    except ValueError:
        seconds = 2.0

    logger.warning(f"Simulating request delay of {seconds} seconds.")
    time.sleep(seconds)
    return JsonResponse({
        "status": "success",
        "message": f"Delayed response by {seconds}s",
        "delay_seconds": seconds
    })


def error_view(request):
    """Simulate server errors (500, exception, etc.)."""
    code = request.GET.get('code', '500')
    logger.error(f"Chaos error triggered with code={code} by client: {request.META.get('REMOTE_ADDR')}")
    
    if code == 'exception':
        raise Exception("Simulated unhandled Chaos Exception!")
        
    return HttpResponseServerError(
        JsonResponse({"error": "Simulated Internal Server Error", "code": 500}),
        content_type="application/json"
    )


def cpu_spike_view(request):
    """Generate temporary CPU intensive workload."""
    try:
        duration = float(request.GET.get('duration', 1.5))
    except ValueError:
        duration = 1.5

    logger.warning(f"Starting CPU spike simulation for {duration} seconds.")
    start_time = time.time()
    count = 0
    while time.time() - start_time < duration:
        # Perform computation
        _ = [math.sqrt(i) * math.sin(i) for i in range(1000)]
        count += 1000

    elapsed = round(time.time() - start_time, 3)
    logger.info(f"CPU spike completed in {elapsed}s with {count} operations.")
    return JsonResponse({
        "status": "success",
        "message": "CPU spike completed",
        "duration_seconds": elapsed,
        "operations": count
    })


def memory_spike_view(request):
    """Generate temporary memory allocation."""
    try:
        mb = int(request.GET.get('mb', 50))
    except ValueError:
        mb = 50

    logger.warning(f"Allocating ~{mb}MB of memory temporarily.")
    # Allocate roughly mb megabytes
    data = bytearray(mb * 1024 * 1024)
    size_mb = len(data) / (1024 * 1024)
    
    logger.info(f"Successfully allocated and releasing {size_mb:.2f}MB memory.")
    del data
    
    return JsonResponse({
        "status": "success",
        "message": f"Allocated and freed {size_mb:.2f}MB",
        "size_mb": size_mb
    })


def logs_view(request):
    """Generate test logs across various levels."""
    level = request.GET.get('level', 'all').lower()
    
    if level == 'debug':
        logger.debug("Chaos test DEBUG log message.")
    elif level == 'info':
        logger.info("Chaos test INFO log message.")
    elif level == 'warning':
        logger.warning("Chaos test WARNING log message.")
    elif level == 'error':
        logger.error("Chaos test ERROR log message.")
    elif level == 'critical':
        logger.critical("Chaos test CRITICAL log message.")
    else:
        logger.debug("Chaos bulk test: DEBUG")
        logger.info("Chaos bulk test: INFO")
        logger.warning("Chaos bulk test: WARNING")
        logger.error("Chaos bulk test: ERROR")
        logger.critical("Chaos bulk test: CRITICAL")

    return JsonResponse({
        "status": "success",
        "message": f"Generated log(s) for level: {level}"
    })