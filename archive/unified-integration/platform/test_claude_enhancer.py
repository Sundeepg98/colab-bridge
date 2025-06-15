#!/usr/bin/env python3
"""
Test script for Claude Enhancer module

This script demonstrates the full capabilities of the Claude enhancement system.
Set your ANTHROPIC_API_KEY environment variable before running.
"""

import asyncio
import json
import os
from src.claude_enhancer import ClaudeEnhancer, EnhancementMode
from src.claude_integration import ClaudeIntegratedOptimizer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


def print_separator():
    """Print a visual separator"""
    console.print("\n" + "="*80 + "\n", style="blue")


async def test_comprehensive_enhancement():
    """Test comprehensive enhancement capabilities"""
    console.print("[bold cyan]Testing Comprehensive Enhancement[/bold cyan]")
    
    enhancer = ClaudeEnhancer()
    
    test_prompts = [
        "A robot walking through a city",
        "Sunset over mountains with birds",
        "An artist painting in their studio"
    ]
    
    for prompt in test_prompts:
        print_separator()
        console.print(f"[yellow]Original Prompt:[/yellow] {prompt}")
        
        result = await enhancer.enhance_prompt(prompt, EnhancementMode.COMPREHENSIVE)
        
        # Display enhanced prompt
        console.print(f"\n[green]Enhanced Prompt:[/green]")
        console.print(Panel(result.enhanced_prompt, expand=False))
        
        # Display scores
        table = Table(title="Quality Scores")
        table.add_column("Dimension", style="cyan")
        table.add_column("Score", style="magenta")
        
        for dimension, score in result.scores.items():
            table.add_row(dimension.replace("_", " ").title(), f"{score:.2f}")
        
        console.print(table)
        
        # Display themes
        if result.themes:
            console.print(f"\n[blue]Identified Themes:[/blue] {', '.join(result.themes[:5])}")
        
        # Display one variation
        if result.variations:
            console.print(f"\n[purple]Sample Variation:[/purple]")
            console.print(Panel(result.variations[0], expand=False))


async def test_different_modes():
    """Test different enhancement modes"""
    console.print("[bold cyan]Testing Different Enhancement Modes[/bold cyan]")
    
    enhancer = ClaudeEnhancer()
    prompt = "A dancer performing on stage"
    
    modes = [
        EnhancementMode.CINEMATIC,
        EnhancementMode.ARTISTIC,
        EnhancementMode.NARRATIVE,
        EnhancementMode.TECHNICAL
    ]
    
    for mode in modes:
        print_separator()
        console.print(f"[yellow]Mode: {mode.value.upper()}[/yellow]")
        
        result = await enhancer.enhance_prompt(prompt, mode)
        
        console.print(f"\n[green]Enhanced ({mode.value}):[/green]")
        console.print(Panel(result.enhanced_prompt, expand=False))
        
        if mode == EnhancementMode.CINEMATIC and result.cinematography:
            console.print(f"\n[blue]Cinematography Notes:[/blue]")
            console.print(Panel(result.cinematography[:300] + "...", expand=False))
        
        if mode == EnhancementMode.NARRATIVE and result.narrative_context:
            console.print(f"\n[blue]Narrative Context:[/blue]")
            console.print(Panel(result.narrative_context[:300] + "...", expand=False))


async def test_sensitive_content_handling():
    """Test sensitive content handling"""
    console.print("[bold cyan]Testing Sensitive Content Handling[/bold cyan]")
    
    enhancer = ClaudeEnhancer()
    
    # Test with potentially sensitive prompt
    prompt = "A warrior in battle defending their homeland"
    
    result = await enhancer.enhance_prompt(prompt, EnhancementMode.SENSITIVE)
    
    print_separator()
    console.print(f"[yellow]Original:[/yellow] {prompt}")
    console.print(f"\n[green]Enhanced (Sensitive Mode):[/green]")
    console.print(Panel(result.enhanced_prompt, expand=False))
    
    if result.content_warnings:
        console.print(f"\n[red]Content Warnings:[/red] {', '.join(result.content_warnings)}")


async def test_iterative_improvement():
    """Test iterative improvement feature"""
    console.print("[bold cyan]Testing Iterative Improvement[/bold cyan]")
    
    enhancer = ClaudeEnhancer()
    
    prompt = "A car driving"  # Intentionally simple
    
    print_separator()
    console.print(f"[yellow]Starting Prompt:[/yellow] {prompt}")
    
    # Get initial scores
    initial_scores = await enhancer._evaluate_prompt(prompt)
    console.print(f"\n[red]Initial Score:[/red] {initial_scores.get('total_score', 0):.2f}")
    
    # Improve iteratively
    improved_prompt, final_scores = await enhancer.evaluate_and_improve(
        prompt, 
        target_score=0.8
    )
    
    console.print(f"\n[green]Improved Prompt:[/green]")
    console.print(Panel(improved_prompt, expand=False))
    console.print(f"\n[green]Final Score:[/green] {final_scores.get('total_score', 0):.2f}")


async def test_batch_processing():
    """Test batch processing capabilities"""
    console.print("[bold cyan]Testing Batch Processing[/bold cyan]")
    
    enhancer = ClaudeEnhancer()
    
    prompts = [
        "A lighthouse in a storm",
        "Children playing in a park",
        "A spaceship landing on Mars",
        "A chef preparing a meal",
        "Northern lights over a forest"
    ]
    
    print_separator()
    console.print("Processing 5 prompts in parallel...")
    
    # Time the batch processing
    import time
    start_time = time.time()
    
    results = await enhancer.batch_enhance(prompts, EnhancementMode.CREATIVE)
    
    elapsed_time = time.time() - start_time
    
    console.print(f"\n[green]Processed {len(results)} prompts in {elapsed_time:.2f} seconds[/green]")
    
    # Show one example
    console.print(f"\n[yellow]Example - Original:[/yellow] {prompts[0]}")
    console.print(f"[green]Enhanced:[/green] {results[0].enhanced_prompt}")


async def test_integration():
    """Test integration with existing system"""
    console.print("[bold cyan]Testing Integration with Existing System[/bold cyan]")
    
    optimizer = ClaudeIntegratedOptimizer()
    
    prompt = "A mysterious forest path"
    
    print_separator()
    result = await optimizer.optimize_with_claude(
        prompt,
        use_existing_optimization=True,
        enhancement_mode=EnhancementMode.COMPREHENSIVE
    )
    
    console.print(f"[yellow]Original:[/yellow] {prompt}")
    
    # Show optimization steps
    console.print("\n[blue]Optimization Steps:[/blue]")
    for step in result["optimization_steps"]:
        console.print(f"\n• {step['step']}:")
        console.print(f"  Result: {step['result'][:100]}...")
    
    console.print(f"\n[green]Final Result:[/green]")
    console.print(Panel(result["final_prompt"], expand=False))


async def main():
    """Run all tests"""
    console.print("[bold magenta]Claude Enhancer Test Suite[/bold magenta]\n")
    
    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        console.print("[red]Error: ANTHROPIC_API_KEY not set in environment[/red]")
        console.print("Please set your Anthropic API key:")
        console.print("  export ANTHROPIC_API_KEY='your-key-here'")
        return
    
    tests = [
        ("Comprehensive Enhancement", test_comprehensive_enhancement),
        ("Different Modes", test_different_modes),
        ("Sensitive Content", test_sensitive_content_handling),
        ("Iterative Improvement", test_iterative_improvement),
        ("Batch Processing", test_batch_processing),
        ("System Integration", test_integration)
    ]
    
    for test_name, test_func in tests:
        try:
            print_separator()
            console.print(f"[bold magenta]Running: {test_name}[/bold magenta]")
            await test_func()
        except Exception as e:
            console.print(f"[red]Error in {test_name}: {str(e)}[/red]")
    
    print_separator()
    console.print("[bold green]All tests completed![/bold green]")


if __name__ == "__main__":
    asyncio.run(main())