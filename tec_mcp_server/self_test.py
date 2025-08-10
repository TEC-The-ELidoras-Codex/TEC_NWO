"""Quick self-test to ensure critical modules import."""
from importlib import import_module

MODULES = [
    'tec_mcp_server.ai_expander',
    'tec_mcp_server.thoughtmap'
]

def main():
    failed = []
    for m in MODULES:
        try:
            import_module(m)
        except Exception as e:  # pragma: no cover
            failed.append((m, repr(e)))
    if failed:
        print("FAIL", failed)
        raise SystemExit(1)
    print("OK modules loaded")

if __name__ == '__main__':
    main()
