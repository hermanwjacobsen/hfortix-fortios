# HFortix-FortiOS

[![PyPI version](https://badge.fury.io/py/hfortix-fortios.svg)](https://pypi.org/project/hfortix-fortios/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Documentation Status](https://readthedocs.org/projects/hfortix-fortios/badge/?version=latest)](https://hfortix-fortios.readthedocs.io/en/latest/)
[![License](https://img.shields.io/badge/License-Proprietary-blue.svg)](LICENSE)
[![Typing: Typed](https://img.shields.io/badge/typing-typed-green.svg)](https://peps.python.org/pep-0561/)

**HFortix-FortiOS** is a modern, fully-typed Python SDK for FortiOS/FortiGate automation with complete API coverage.

## 🚀 Quick Start

```bash
pip install hfortix-fortios
```

```python
from hfortix_fortios import FortiOS

# Connect to your FortiGate
with FortiOS(host="192.168.1.99", token="your-api-token") as fgt:
    # Create firewall address
    fgt.api.cmdb.firewall.address.post(
        name="web-server",
        subnet="10.0.1.100/32",
        comment="Production web server"
    )
    
    # Create firewall policy with simplified syntax
    fgt.api.cmdb.firewall.policy.post(
        name="Allow-Web-Traffic",
        srcintf=["internal"],      # Auto-converted to FortiOS format
        dstintf=["wan1"],
        srcaddr=["all"],
        dstaddr=["web-server"],
        service=["HTTP", "HTTPS"],
        action="accept",
        nat="enable"
    )
```

## ✨ Key Features

- **🎯 Complete API Coverage** - 1,348 endpoints across CMDB, Monitor, Log, and Service APIs
- **💪 Fully Typed** - Complete type hints with .pyi stubs for excellent IDE support
- **⚡ Modern & Fast** - Async/await support with httpx, HTTP/2, connection pooling
- **🛡️ Production Ready** - Comprehensive error handling, validation, retry logic, rate limiting
- **🔄 Simplified Syntax** - Simple list format auto-converts to FortiOS dict format
- **📦 Batch Transactions** - Atomic configuration changes with automatic commit/rollback (v0.5.152+)
- **🔍 API Inspection** - Debug and audit API interactions (v0.5.152+)
- **🌐 FortiManager Proxy** - Manage multiple FortiGates through FortiManager

## 📊 API Coverage

**FortiOS 7.6.5 - 100% Coverage (1,348 endpoints)**

- **561 CMDB endpoints** - Configuration database management (100% typed)
- **490 Monitor endpoints** - Real-time monitoring and statistics (partial types)  
- **286 Log endpoints** - Log retrieval and analysis (partial types)
- **11 Service endpoints** - Service operations (100% typed)

All endpoints are auto-generated with complete schema coverage.

## 📚 Documentation

- **Full Documentation**: https://hfortix-fortios.readthedocs.io
- **Quickstart Guide**: See [QUICKSTART.md](QUICKSTART.md)
- **Examples**: See [EXAMPLES.md](EXAMPLES.md)
- **API Reference**: https://hfortix-fortios.readthedocs.io/en/latest/api-reference/

## 🔗 Related Packages

This package is part of the HFortix SDK ecosystem:

- **[hfortix-core](https://github.com/hermanwjacobsen/hfortix-core)** - Core HTTP client and utilities
- **[hfortix](https://github.com/hermanwjacobsen/hfortix)** - Meta package to install all components

## 📄 License

Proprietary license. All rights reserved.

## 🤝 Support

- **Issues**: https://github.com/hermanwjacobsen/hfortix-fortios/issues
- **PyPI**: https://pypi.org/project/hfortix-fortios/

---

**Version**: 0.5.154-beta  
**FortiOS Support**: 7.6.5  
**Python**: 3.10+
