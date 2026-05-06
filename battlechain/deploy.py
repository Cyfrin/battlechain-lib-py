"""Deploy helpers via BattleChainDeployer (or CreateX off-chain).

Mirrors src/BCDeploy.sol from cyfrin/battlechain-lib. Tracks all deployed
addresses so they can be passed to Safe Harbor agreement builders.

Boa-first: every helper assumes a boa environment with a configured EOA.
"""

from __future__ import annotations

from battlechain import _boa

# Module-level deployment tracker. Mirrors `address[] private _deployedContracts`
# in BCDeploy.sol — it persists for the duration of a script run, which matches
# the moccasin `def moccasin_main()` pattern of one process per invocation.
_deployed: list[str] = []


def bc_deploy_create(init_code: bytes) -> str:
    """Deploy via CREATE.

    Mirrors `BCDeploy.bcDeployCreate(initCode)`. Routes through:
      - BattleChainDeployer on BattleChain (auto-registers with AttackRegistry)
      - CreateX on any other supported chain
    """
    deployer = _boa.deployer()
    address = deployer.deployCreate(init_code)
    _deployed.append(address)
    return address


def bc_deploy_create2(salt: bytes, init_code: bytes) -> str:
    """Deploy via CREATE2 (deterministic address, salt + bytecode).

    Mirrors `BCDeploy.bcDeployCreate2(salt, initCode)`.
    """
    if len(salt) != 32:
        raise ValueError(f"salt must be 32 bytes, got {len(salt)}")
    deployer = _boa.deployer()
    address = deployer.deployCreate2(salt, init_code)
    _deployed.append(address)
    return address


def bc_deploy_create3(salt: bytes, init_code: bytes) -> str:
    """Deploy via CREATE3 (address depends only on salt, not bytecode).

    Mirrors `BCDeploy.bcDeployCreate3(salt, initCode)`.
    """
    if len(salt) != 32:
        raise ValueError(f"salt must be 32 bytes, got {len(salt)}")
    deployer = _boa.deployer()
    address = deployer.deployCreate3(salt, init_code)
    _deployed.append(address)
    return address


def deployed_contracts() -> tuple[str, ...]:
    """Return all addresses deployed this session via `bc_deploy_*` helpers.

    Mirrors `BCDeploy.getDeployedContracts()`.
    """
    return tuple(_deployed)


def reset_deployments() -> None:
    """Clear the tracked deployment list. Useful between independent runs/tests."""
    _deployed.clear()


def track_deployment(address: str) -> None:
    """Manually record an address as if it had been deployed via `bc_deploy_*`.

    Useful when a contract was deployed before this session started (e.g., a
    pre-existing token) but should still appear in the agreement's scope.
    """
    _deployed.append(address)


__all__ = [
    "bc_deploy_create",
    "bc_deploy_create2",
    "bc_deploy_create3",
    "deployed_contracts",
    "reset_deployments",
    "track_deployment",
]
