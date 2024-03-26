# PUNKZ

This is a package developed by Devpunks that contains some utilities for our projects.
At the moment it includes:

- Cache System (local, AWS S3 bucket)
- Processor Framework (very experimental)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

You can easily install this package using pip.

```
pip install punkz
```

## Usage

There are many utilities contained in this package.

### Cache System

#### Local Caching

Example Code for local caching.

```
from punkz.core import Cache, LocalCacheProvider
from punkz.packages import get_logger

logger = get_logger("cache_logger")
provider = LocalCacheProvider(".cache", logger=logger)
my_cache = Cache(
    provider=provider,
    cache_instance_id="test",
    expiration="1d",
    logger=logger
    )

@my_cache.cache
def my_func(x):
    return x + 1

print(my_func(99))
```

Note: not passing logger to the Cache or the Provider is possible and if done
it will simply deactivate logging and printing.

#### Caching on AWS

Example Code for caching on an AWS S3 bucket.

```
from punkz.core import Cache, AWSS3CacheProvider
from punkz.packages import get_logger

logger = get_logger("cache_logger")
provider = AWSS3CacheProvider(
    bucket_name="your-bucket-name",
    access_key_id="your-access-key-id",
    secret_access_key="your-secret-access-key",
    logger=logger
    )
my_cache = Cache(
    provider=provider,
    cache_instance_id="test",
    expiration="1d",
    logger=logger
    )

@my_cache.cache
def my_func(x):
    return x + 1

print(my_func(99))
```

### Processor Framework

This is still a work in progress functionality. Documentation will be added
in future releases.

## License

This package is released under MIT License.

## Disclaimer

This package is highly experimental and it will be further expanded and refactored in the future.
