# Security model

Workload identity, peer verification, deny-by-default policy, rotation and audit.

## Detailed reference

[Read the complete security model reference](sources/platform/docs/security-model.html), copied from the platform repository at its recorded revision. The reference includes detailed tables, behavior and examples.

## Apply it to a module

The framework establishes common behavior; [module references](modules/index.html) document additional configuration and interfaces. [Architecture workflows](architecture/index.html) connect those details to end-to-end operations.

[Platform version and source information](modules/platform.html) · [Native configuration setup](how-to/native-prerequisites.html)

## Assign and verify permissions

Permissions use the qualified `module:resource:action` form in custom roles, for example `dns:zones:read`. The same local name in two modules represents two different grants. Each [module reference](modules/index.html) lists every declared permission, its purpose, UI actions and matching API operations at the recorded revision.

1. Open Auth’s permission catalogue and select the intended module. Inspect the permission descriptions and the catalogue’s grantable status for your account.
2. Choose a provided module role or create a custom role containing the exact qualified permissions needed. Provided module roles are locked; clone one if you need a different permission set. Do not assume that an action named `manage` grants every other action.
3. Assign the role to the user or an appropriate group in the intended tenant. Check inherited group roles as well as direct user roles. Role assignment is constrained by what the assigning actor can grant.
4. Where the module uses document, folder, secret, channel or template sharing, grant the required access on the resource too. A module API permission and a resource relationship are separate checks.
5. Test with the intended user: verify an allowed read or action, then verify an ungranted action and an inaccessible resource are denied. Check the actual API response as well as navigation visibility. Hidden controls are not authorization enforcement.

Gateway routes declare their module permissions; the server may additionally check tenant scope, ownership, relationships, actor type and workflow state. Auth’s own console instead authenticates its session and authorizes internally. Service-to-service calls use workload identity and peer policy and may have consumer-specific restrictions. Assigning a human role does not authorize a mesh peer.

For a permission-denied response, check the selected tenant, direct and group roles, the exact qualified permission, resource grants and their expiry/inheritance, and any module-specific restrictions. Consult the module’s catalogue and source links before broadening a role. Platform administration, tenant administration and resource ownership are separate scopes.
