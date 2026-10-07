# Module directory

Every verified v4 component, grouped by its role. Services share the platform framework and UI contracts; their release versions remain independent.

## Foundation

<div class="cards module-cards">
<a class="card" href="modules/platform.html"><span class="card-label">PLATFORM / V4</span><strong>Go-Tangra Platform</strong><p>Secure service framework, shared UI kit and development stack.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
</div>

## Control plane

<div class="cards module-cards">
<a class="card" href="modules/auth.html"><span class="card-label">AUTH / V4</span><strong>Auth</strong><p>Tenant identity, sessions, tokens and fine-grained authorization.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/portal.html"><span class="card-label">PORTAL / V4</span><strong>Portal / Gateway</strong><p>Public application edge, leased module registry and federated shell.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/lcm.html"><span class="card-label">LCM / V4</span><strong>LCM</strong><p>Mesh certificate authority, SVID enrollment and certificate lifecycle.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/warden.html"><span class="card-label">WARDEN / V4</span><strong>Warden</strong><p>Vault-backed secrets management and controlled credential sharing.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
</div>

## Platform services

<div class="cards module-cards">
<a class="card" href="modules/notification.html"><span class="card-label">NOTIFICATION / V4</span><strong>Notification</strong><p>Central SMTP notifications, inbox messages and delivery management.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/scheduler.html"><span class="card-label">SCHEDULER / V4</span><strong>Scheduler</strong><p>Typed tenant and platform jobs, cron scheduling, retries and history.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
</div>

## Infrastructure

<div class="cards module-cards">
<a class="card" href="modules/inventory.html"><span class="card-label">INVENTORY / V4</span><strong>Inventory</strong><p>Endpoint agents, hardware/software snapshots and change tracking.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/ipam.html"><span class="card-label">IPAM / V4</span><strong>IPAM</strong><p>IP addresses, networks, active discovery and IPMI/KVM operations.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/dns.html"><span class="card-label">DNS / V4</span><strong>DNS</strong><p>PowerDNS management, DNS records, IPAM synchronization and ACME challenges.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/deployer.html"><span class="card-label">DEPLOYER / V4</span><strong>Deployer</strong><p>Distribute certificates to infrastructure targets and track deployment.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
</div>

## Business modules

<div class="cards module-cards">
<a class="card" href="modules/asset.html"><span class="card-label">ASSET / V4</span><strong>Asset</strong><p>IT asset lifecycle, consumables, licenses, insurance and depreciation.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/paperless.html"><span class="card-label">PAPERLESS / V4</span><strong>Paperless</strong><p>Documents, object storage, text extraction, full-text search and sharing.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/ticket.html"><span class="card-label">TICKET / V4</span><strong>Ticket</strong><p>Email helpdesk, conversations, mailboxes and triage rules.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/signing.html"><span class="card-label">SIGNING / V4</span><strong>Signing</strong><p>PDF templates, signing submissions, personal and qualified signatures.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/hr.html"><span class="card-label">HR / V4</span><strong>HR</strong><p>Leave requests, allowances, team calendars and signing integration.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
</div>

## Communications

<div class="cards module-cards">
<a class="card" href="modules/sms-gw.html"><span class="card-label">SMS-GW / V4</span><strong>SMS Gateway</strong><p>Hermes SMS API, carrier receipts, callbacks and tenant management.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
<a class="card" href="modules/asterisk.html"><span class="card-label">ASTERISK / V4</span><strong>Asterisk</strong><p>Read-only PBX observation, call history, recordings and RTP diagnostics.</p><span class="card-arrow" aria-hidden="true">Read module reference ↗</span></a>
</div>

## Shared libraries and integrations

[Platform](modules/platform.html) also documents the consumed framework packages, service SDKs, UI kit and optional audit/policy contrib modules. External storage, DNS, mail and PBX services are dependencies rather than invented Go-Tangra modules.
