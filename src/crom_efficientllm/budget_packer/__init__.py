from .packer import Chunk, budget_pack, pack_summary

# Import enhanced_greedy_pack from parent module
def _import_enhanced_greedy_pack():
    """Lazy import to avoid circular dependency"""
    import os
    import sys
    parent_path = os.path.dirname(os.path.dirname(__file__))
    budget_packer_path = os.path.join(parent_path, 'budget_packer.py')

    if os.path.exists(budget_packer_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("budget_packer_standalone", budget_packer_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.enhanced_greedy_pack
    else:
        raise ImportError("enhanced_greedy_pack not found")

# Lazy loading
enhanced_greedy_pack = _import_enhanced_greedy_pack()

__all__ = ["Chunk", "budget_pack", "pack_summary", "enhanced_greedy_pack"]
