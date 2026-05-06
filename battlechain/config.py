"""Address registry for BattleChain contracts, resolved by chain ID.

Mirrors src/BCConfig.sol and src/BCBase.sol from cyfrin/battlechain-lib.
On supported chains, addresses resolve from the canonical registry.
On unsupported chains (Anvil, forks), use `set_overrides()` to provide them manually.
"""

from dataclasses import dataclass, field

from battlechain import createx_chains
from battlechain.errors import (
    CreateXNotAvailableError,
    UnsupportedChainForQueryError,
    UnsupportedChainIdError,
    ZeroAddressError,
)

# -----------------------------------------------------------------------------
# Chain IDs
# -----------------------------------------------------------------------------

MAINNET_CHAIN_ID = 626
TESTNET_CHAIN_ID = 627

# -----------------------------------------------------------------------------
# CAIP-2 chain ID strings
# -----------------------------------------------------------------------------

MAINNET_CAIP2 = "eip155:626"
TESTNET_CAIP2 = "eip155:627"

# -----------------------------------------------------------------------------
# CreateX — well-known address, same on all supported chains.
# See createx_chains.py for the full list.
# -----------------------------------------------------------------------------

WELL_KNOWN_CREATEX = "0xba5Ed099633D3B313e4D5F7bdc1305d3c28ba5Ed"

# -----------------------------------------------------------------------------
# Safe Harbor agreement URIs
# -----------------------------------------------------------------------------

SAFE_HARBOR_V3_URI = "ipfs://bafkreiernns2f4nv2uzvwtzjc2jboyivsu2mixz33y3xo7cvtllsuao6jy"
BATTLECHAIN_SAFE_HARBOR_URI = "ipfs://bafkreifgln3ir67woluatpwn3b65gjkrbmoq6jgzzotm3anas3vvq4yp4m"

# -----------------------------------------------------------------------------
# Block explorer
# -----------------------------------------------------------------------------

TESTNET_RPC_URL = "https://testnet.battlechain.com"

# Bare host: used by the BattleChain-specific routes (e.g.,
# `/battlechain/agreement/by-contract/<addr>`) consumed by the BCQuery helpers.
TESTNET_EXPLORER_HOST = "https://block-explorer-api.testnet.battlechain.com"
MAINNET_EXPLORER_HOST = "https://block-explorer-api.battlechain.com"

# Etherscan-compatible API: used by `verify.verify_contract` to submit source.
TESTNET_EXPLORER_API = f"{TESTNET_EXPLORER_HOST}/api"
MAINNET_EXPLORER_API = f"{MAINNET_EXPLORER_HOST}/api"


@dataclass(frozen=True)
class BcNetworkConfig:
    """Resolved network configuration for a BattleChain or CreateX-supported chain."""

    chain_id: int
    caip2: str
    registry: str
    factory: str
    attack_registry: str
    deployer: str
    create_x: str
    safe_harbor_uri: str


# -----------------------------------------------------------------------------
# Testnet (627) addresses — canonical, from BCConfig.sol
# -----------------------------------------------------------------------------

TESTNET_REGISTRY = "0x0a652e265336a0296816aC4D8400880e3E537C24"
TESTNET_AGREEMENT_FACTORY = "0x2Bee2970f10FDc2aeA28662BB6F6A501278Ebd46"
TESTNET_ATTACK_REGISTRY = "0xdD029a6374095EEb4c47a2364Ce1D0f47f007350"
TESTNET_DEPLOYER = "0x74269804941119554460956f16Fe82Fbe4B90448"
TESTNET_CREATEX = "0xf1Ebfaa992854ECcB01Ac1F60e5b5279095cca7F"
TESTNET_REGISTRY_IMPL = "0xCd8B924D0F43C26E99dDE7a2C7A47d9fAf0c10bB"
TESTNET_AGREEMENT_FACTORY_IMPL = "0x7D14c46539f673152857Ea647E66E5AD5f820043"
TESTNET_ATTACK_REGISTRY_IMPL = "0x34328AeBd4e3b173B71144AB29F4509E6816277c"
TESTNET_MOCK_REGISTRY_MODERATOR = "0x1bC64E6F187a47D136106784f4E9182801535BD3"

bc_testnet = BcNetworkConfig(
    chain_id=TESTNET_CHAIN_ID,
    caip2=TESTNET_CAIP2,
    registry=TESTNET_REGISTRY,
    factory=TESTNET_AGREEMENT_FACTORY,
    attack_registry=TESTNET_ATTACK_REGISTRY,
    deployer=TESTNET_DEPLOYER,
    create_x=TESTNET_CREATEX,
    safe_harbor_uri=BATTLECHAIN_SAFE_HARBOR_URI,
)

# Mainnet (626) addresses are TBD per the official docs.
_KNOWN_NETWORKS: dict[int, BcNetworkConfig] = {
    TESTNET_CHAIN_ID: bc_testnet,
}


# -----------------------------------------------------------------------------
# Override registry for local Anvil / unsupported chains
# (mirrors `BCBase._setBcAddresses(...)`)
# -----------------------------------------------------------------------------

@dataclass
class _OverrideState:
    overrides: dict[int, BcNetworkConfig] = field(default_factory=dict)


_state = _OverrideState()


def set_overrides(
    chain_id: int,
    *,
    registry: str,
    factory: str,
    attack_registry: str,
    deployer: str,
    create_x: str | None = None,
    safe_harbor_uri: str = BATTLECHAIN_SAFE_HARBOR_URI,
    caip2: str | None = None,
) -> BcNetworkConfig:
    """Register address overrides for a chain (e.g., Anvil 31337, forks).

    Mirrors `BCBase._setBcAddresses(registry, factory, attackRegistry, deployer)`.
    Returns the resolved BcNetworkConfig.
    """
    for name, value in [
        ("registry", registry),
        ("factory", factory),
        ("attack_registry", attack_registry),
        ("deployer", deployer),
    ]:
        if not value or int(value, 16) == 0:
            raise ZeroAddressError(f"{name} cannot be the zero address")

    config = BcNetworkConfig(
        chain_id=chain_id,
        caip2=caip2 or f"eip155:{chain_id}",
        registry=registry,
        factory=factory,
        attack_registry=attack_registry,
        deployer=deployer,
        create_x=create_x or WELL_KNOWN_CREATEX,
        safe_harbor_uri=safe_harbor_uri,
    )
    _state.overrides[chain_id] = config
    return config


def clear_overrides(chain_id: int | None = None) -> None:
    """Clear overrides for one chain, or all chains if `chain_id` is None."""
    if chain_id is None:
        _state.overrides.clear()
    else:
        _state.overrides.pop(chain_id, None)


# -----------------------------------------------------------------------------
# Resolution
# -----------------------------------------------------------------------------

def get_network_config(chain_id: int) -> BcNetworkConfig:
    """Resolve the network config for a chain ID.

    Lookup order: registered overrides → known BattleChain networks.
    Raises UnsupportedChainIdError if neither has it.
    """
    if chain_id in _state.overrides:
        return _state.overrides[chain_id]
    if chain_id in _KNOWN_NETWORKS:
        return _KNOWN_NETWORKS[chain_id]
    raise UnsupportedChainIdError(chain_id)


def is_battlechain(chain_id: int) -> bool:
    """Return True if this is a BattleChain network (mainnet or testnet).

    Mirrors `BCConfig.isBattleChain()`.
    """
    return chain_id in {MAINNET_CHAIN_ID, TESTNET_CHAIN_ID}


def caip2_chain_id(chain_id: int) -> str:
    """Return the CAIP-2 chain ID string for a chain.

    Mirrors `BCConfig.caip2ChainId()` for known BattleChain networks; falls back
    to `eip155:<chainId>` for any other chain (matching `defaultAgreementDetails`).
    """
    if chain_id in _state.overrides:
        return _state.overrides[chain_id].caip2
    if chain_id == MAINNET_CHAIN_ID:
        return MAINNET_CAIP2
    if chain_id == TESTNET_CHAIN_ID:
        return TESTNET_CAIP2
    return f"eip155:{chain_id}"


def registry_address(chain_id: int) -> str:
    """Return the BattleChainSafeHarborRegistry address for a chain."""
    return get_network_config(chain_id).registry


def agreement_factory_address(chain_id: int) -> str:
    """Return the AgreementFactory address for a chain."""
    return get_network_config(chain_id).factory


def attack_registry_address(chain_id: int) -> str:
    """Return the AttackRegistry address for a chain."""
    return get_network_config(chain_id).attack_registry


def deployer_address(chain_id: int) -> str:
    """Return the deployer address for a chain.

    On BattleChain networks: the BattleChainDeployer (CreateX + AttackRegistry registration).
    On other chains: CreateX at the well-known address (if supported).
    """
    if chain_id in _state.overrides:
        return _state.overrides[chain_id].deployer
    if is_battlechain(chain_id):
        return get_network_config(chain_id).deployer
    return create_x_address(chain_id)


def create_x_address(chain_id: int) -> str:
    """Return the CreateX address for a chain.

    Mirrors `BCConfig.createX()`. Raises CreateXNotAvailableError if the chain
    is not in the CreateX-supported registry.
    """
    if chain_id in _state.overrides:
        return _state.overrides[chain_id].create_x
    if chain_id == TESTNET_CHAIN_ID:
        return TESTNET_CREATEX
    if createx_chains.is_supported(chain_id):
        return WELL_KNOWN_CREATEX
    raise CreateXNotAvailableError(chain_id)


def safe_harbor_uri(chain_id: int) -> str:
    """Return the default Safe Harbor agreement URI for a chain.

    BattleChain networks use the BattleChain-specific URI; all others use V3.
    """
    if is_battlechain(chain_id):
        return BATTLECHAIN_SAFE_HARBOR_URI
    return SAFE_HARBOR_V3_URI


def explorer_host(chain_id: int) -> str:
    """Return the bare BattleChain block explorer host for a chain.

    Used by the BCQuery off-chain agreement lookup at
    `<host>/battlechain/agreement/by-contract/<address>`.

    Mirrors `BCQuery._explorerApiUrl()` and raises `UnsupportedChainForQueryError`
    for non-BattleChain chains, matching `BCQuery__UnsupportedChainForQuery`.
    """
    if chain_id == TESTNET_CHAIN_ID:
        return TESTNET_EXPLORER_HOST
    if chain_id == MAINNET_CHAIN_ID:
        return MAINNET_EXPLORER_HOST
    raise UnsupportedChainForQueryError(chain_id)


def explorer_api(chain_id: int) -> str:
    """Return the Etherscan-compatible API URL for a chain.

    Used by `verify.verify_contract` to submit source for verification.
    """
    return f"{explorer_host(chain_id)}/api"


__all__ = [
    "BATTLECHAIN_SAFE_HARBOR_URI",
    "BcNetworkConfig",
    "MAINNET_CAIP2",
    "MAINNET_CHAIN_ID",
    "MAINNET_EXPLORER_API",
    "MAINNET_EXPLORER_HOST",
    "SAFE_HARBOR_V3_URI",
    "TESTNET_AGREEMENT_FACTORY",
    "TESTNET_AGREEMENT_FACTORY_IMPL",
    "TESTNET_ATTACK_REGISTRY",
    "TESTNET_ATTACK_REGISTRY_IMPL",
    "TESTNET_CAIP2",
    "TESTNET_CHAIN_ID",
    "TESTNET_CREATEX",
    "TESTNET_DEPLOYER",
    "TESTNET_EXPLORER_API",
    "TESTNET_EXPLORER_HOST",
    "TESTNET_MOCK_REGISTRY_MODERATOR",
    "TESTNET_REGISTRY",
    "TESTNET_REGISTRY_IMPL",
    "TESTNET_RPC_URL",
    "WELL_KNOWN_CREATEX",
    "agreement_factory_address",
    "attack_registry_address",
    "bc_testnet",
    "caip2_chain_id",
    "clear_overrides",
    "create_x_address",
    "deployer_address",
    "explorer_api",
    "explorer_host",
    "get_network_config",
    "is_battlechain",
    "registry_address",
    "safe_harbor_uri",
    "set_overrides",
]
