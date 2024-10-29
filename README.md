# Alibaba Register DNS

A Python tool for automating DNS registration with Alibaba Cloud and Cloudflare, allowing seamless DNS entry management across both platforms.

## Features

- **DNS Registration Automation**: Streamlines the creation and registration of DNS zones.
- **Alibaba Cloud Integration**: Adds all domains to Alibaba for email sending.
- **Cloudflare Integration**: Manages DNS zones within Cloudflare.

## Reason or Motivation

Managing DNS entries across multiple platforms can be complex. This tool simplifies DNS setup for Alibaba and Cloudflare, enhancing email deliverability and management.

## Tech Stack

- **Python**
- **Alibaba SDK**
- **Cloudflare Library**

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/devraider/alibaba-register-dns.git
    cd alibaba-register-dns
    ```
2. Configure your Alibaba and Cloudflare credentials.
3. Run the script:
    ```bash
    python alibaba_config_domains.py
    ```
