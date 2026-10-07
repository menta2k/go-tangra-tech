# Go-Tangra documentation

## A shared foundation. Your choice of modules.

Go-Tangra v4 brings infrastructure management, operational tools and business workflows into a connected platform. Services live in independent repositories and share the Freya framework, a common security model and a unified web interface. Deploy the modules you need; follow their dependencies when adding more.

<div class="cards">
<a class="card" href="architecture/index.html"><span class="card-label">01 / UNDERSTAND</span><strong>Explore the architecture</strong><p>Follow identities, requests and data through the control plane and service mesh.</p><span class="card-arrow" aria-hidden="true">↗</span></a>
<a class="card" href="modules/index.html"><span class="card-label">02 / DISCOVER</span><strong>Find your module</strong><p>Browse every v4 component, its responsibilities, dependencies and interfaces.</p><span class="card-arrow" aria-hidden="true">↗</span></a>
<a class="card" href="how-to/index.html"><span class="card-label">03 / INSTALL</span><strong>Bring it online</strong><p>Choose a Docker deployment or run a native service with host-managed dependencies.</p><span class="card-arrow" aria-hidden="true">↗</span></a>
</div>

## What you can build

- **Operate infrastructure** with Inventory, IPAM, DNS, Deployer and Asset.
- **Connect business workflows** with Paperless, Ticket, Signing and HR.
- **Coordinate platform work** with Notification and Scheduler.
- **Integrate communications** with SMS Gateway and a read-only Asterisk observer.

Auth, Portal, LCM and Warden supply identity, the application edge, mesh certificates and controlled secrets access. The [module directory](modules/index.html) explains which components each service needs.

## Security is part of the foundation

Freya supplies SPIFFE workload identity, encrypted and mutually authenticated channels, deny-by-default service policies, automatic identity rotation, audit and observability. Modules build on those capabilities rather than reimplementing service trust. [Read the security model](architecture/security.html).

## Start with one clear path

New to the system? [Start here](getting-started.html). Already know your module? [Choose an installation guide](how-to/index.html). Building an integration? [Trace the architecture](architecture/index.html) and open the module's configuration and API reference.

This documentation describes **v4 source snapshots recorded on 5 October 2026**. Services have independent versions; the [platform reference](modules/platform.html) records the source revisions. Local source tags do not establish a tested release combination or published image availability.
