import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from prompt_generator import (
    SoraPromptGenerator, PromptElements, PromptEnhancer,
    CameraMovement, ShotType, Style, Lighting
)
from prompt_optimizer import PromptOptimizer, ContentContext
from context_framing import ContextFramingSystem
from language_templates import LanguageTemplates, ProfessionalContext
from advanced_context import AdvancedContextElaborator, MatureThemeHandler
from narrative_enhancer import NarrativeEnhancer, ComplexThemeProcessor
from bold_concepts import BoldConceptHandler, ExperimentalArtFramer, ConceptualBoundaryPusher


console = Console()


@click.group()
def cli():
    """Sora AI Prompt Generation Tool"""
    pass


@cli.command()
@click.option('--subject', '-s', required=True, help='Main subject of the video')
@click.option('--action', '-a', help='Action being performed')
@click.option('--setting', help='Location or environment')
@click.option('--camera', type=click.Choice([c.name.lower() for c in CameraMovement]), help='Camera movement')
@click.option('--shot', type=click.Choice([s.name.lower() for s in ShotType]), help='Shot type')
@click.option('--style', type=click.Choice([s.name.lower() for s in Style]), help='Visual style')
@click.option('--lighting', type=click.Choice([l.name.lower() for l in Lighting]), help='Lighting style')
@click.option('--mood', help='Overall mood or atmosphere')
@click.option('--variations', '-v', type=int, default=0, help='Number of variations to generate')
def generate(subject, action, setting, camera, shot, style, lighting, mood, variations):
    """Generate a Sora AI prompt"""
    
    generator = SoraPromptGenerator()
    
    elements = PromptElements(
        subject=subject,
        action=action,
        setting=setting,
        camera_movement=CameraMovement[camera.upper()] if camera else None,
        shot_type=ShotType[shot.upper()] if shot else None,
        style=Style[style.upper()] if style else None,
        lighting=Lighting[lighting.upper()] if lighting else None,
        mood=mood
    )
    
    main_prompt = generator.generate(elements)
    
    console.print(Panel(main_prompt, title="Generated Prompt", border_style="green"))
    
    if variations > 0:
        console.print("\n[bold]Variations:[/bold]")
        variation_prompts = generator.generate_variations(elements, variations)
        for i, prompt in enumerate(variation_prompts, 1):
            console.print(f"[cyan]{i}.[/cyan] {prompt}")


@cli.command()
def examples():
    """Show example prompts"""
    
    examples_data = [
        {
            "subject": "a cyberpunk cat",
            "action": "walking through neon-lit streets",
            "style": "cyberpunk",
            "lighting": "neon",
            "mood": "mysterious"
        },
        {
            "subject": "a vintage car",
            "action": "driving along a coastal road",
            "camera": "tracking",
            "style": "cinematic",
            "lighting": "golden_hour"
        },
        {
            "subject": "cherry blossoms",
            "action": "falling gently",
            "shot": "close_up",
            "style": "minimalist",
            "mood": "serene"
        }
    ]
    
    generator = SoraPromptGenerator()
    
    table = Table(title="Example Prompts", show_header=True, header_style="bold magenta")
    table.add_column("Elements", style="cyan", width=30)
    table.add_column("Generated Prompt", style="green")
    
    for example in examples_data:
        elements = PromptElements(
            subject=example.get("subject"),
            action=example.get("action"),
            camera_movement=CameraMovement[example["camera"].upper()] if "camera" in example else None,
            shot_type=ShotType[example["shot"].upper()] if "shot" in example else None,
            style=Style[example["style"].upper()] if "style" in example else None,
            lighting=Lighting[example["lighting"].upper()] if "lighting" in example else None,
            mood=example.get("mood")
        )
        
        elements_str = f"Subject: {elements.subject}\n"
        if elements.action:
            elements_str += f"Action: {elements.action}\n"
        if elements.style:
            elements_str += f"Style: {elements.style.name}"
        
        prompt = generator.generate(elements)
        table.add_row(elements_str, prompt)
    
    console.print(table)


@cli.command()
@click.option('--input', '-i', required=True, help='Your prompt idea')
@click.option('--context', '-c', type=click.Choice([c.value for c in ContentContext]), help='Content context')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed optimization steps')
def optimize(input, context, verbose):
    """Optimize a prompt for better acceptance"""
    
    optimizer = PromptOptimizer()
    framing_system = ContextFramingSystem()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing prompt...", total=3)
        
        # Step 1: Optimize
        progress.update(task, advance=1, description="Optimizing language...")
        content_context = ContentContext[context.upper()] if context else None
        result = optimizer.optimize(input, content_context)
        
        # Step 2: Frame
        progress.update(task, advance=1, description="Applying context framing...")
        framing_result = framing_system.apply_framing(result.optimized_prompt)
        
        # Step 3: Final touches
        progress.update(task, advance=1, description="Finalizing...")
    
    console.print("\n[bold cyan]Optimization Results[/bold cyan]\n")
    
    console.print(Panel(input, title="Original Prompt", border_style="red"))
    console.print(Panel(framing_result["framed"], title="Optimized Prompt", border_style="green"))
    
    console.print(f"\n[yellow]Success Likelihood:[/yellow] {framing_result['expected_success_rate']:.1%}")
    console.print(f"[yellow]Context Applied:[/yellow] {framing_result['template_used']}")
    
    if verbose and result.suggestions:
        console.print("\n[bold]Optimization Steps:[/bold]")
        for suggestion in result.suggestions:
            console.print(f"  • {suggestion}")
    
    # Show improvement suggestions
    suggestions = framing_system.suggest_improvements(input)
    if suggestions:
        console.print("\n[bold]Additional Suggestions:[/bold]")
        for suggestion in suggestions[:3]:
            console.print(f"\n[cyan]Issue:[/cyan] {suggestion['issue']}")
            console.print(f"[green]Fix:[/green] {suggestion['suggestion']}")


@cli.command()
@click.option('--prompt', '-p', required=True, help='Complex prompt to elaborate')
@click.option('--depth', '-d', type=click.Choice(['basic', 'advanced', 'maximum']), default='advanced', help='Elaboration depth')
@click.option('--theme', '-t', type=click.Choice(['romance', 'spiritual', 'controversial', 'bold', 'general']), help='Theme type')
def elaborate(prompt, depth, theme):
    """Deeply elaborate complex themes with rich context"""
    
    elaborator = AdvancedContextElaborator()
    narrative_enhancer = NarrativeEnhancer()
    theme_processor = ComplexThemeProcessor()
    bold_handler = BoldConceptHandler()
    experimental_framer = ExperimentalArtFramer()
    boundary_pusher = ConceptualBoundaryPusher()
    
    console.print("[bold cyan]Advanced Context Elaboration[/bold cyan]\n")
    
    # Process based on theme type
    if theme == 'bold':
        # Handle bold concepts
        processed = bold_handler.frame_bold_concept(prompt)
        processed = experimental_framer.frame_experimental_work(processed)
        processed = boundary_pusher.push_conceptual_boundaries(processed)
        
        # Add theoretical justification
        processed = bold_handler.add_theoretical_justification(processed)
        processed = bold_handler.add_radical_art_context(processed)
    else:
        # Standard complex theme processing
        processed = theme_processor.process_complex_theme(prompt)
    
    # Apply elaboration
    result = elaborator.elaborate_context(processed, theme)
    
    # Add narrative enhancement based on depth
    if depth in ['advanced', 'maximum']:
        result.final_prompt = narrative_enhancer.create_full_narrative_context(
            result.final_prompt, 
            ['literary', 'production', 'artistic']
        )
    
    if depth == 'maximum':
        # Add cultural bridge and emotional depth
        result.final_prompt = narrative_enhancer.create_cultural_bridge(result.final_prompt)
        result.final_prompt = narrative_enhancer.add_emotional_depth(result.final_prompt)
        
        # For bold concepts, add extra experimental layers
        if theme == 'bold':
            result.final_prompt = experimental_framer.add_bold_artistic_merit(result.final_prompt)
    
    # Display results
    console.print(Panel(prompt, title="Original Prompt", border_style="yellow"))
    console.print(Panel(result.final_prompt, title="Elaborated Prompt", border_style="green"))
    
    console.print(f"\n[yellow]Confidence Score:[/yellow] {result.confidence_score:.1%}")
    console.print(f"[yellow]Narrative Frame:[/yellow] {result.narrative_frame}")
    console.print(f"[yellow]Cultural Context:[/yellow] {result.cultural_context}")
    
    # Show breakdown if maximum depth
    if depth == 'maximum':
        console.print("\n[bold]Context Layers Applied:[/bold]")
        console.print("  • Complex theme processing")
        console.print("  • Narrative framework elaboration")
        console.print("  • Literary and cultural references")
        console.print("  • Production value context")
        console.print("  • Artistic merit justification")
        console.print("  • Cultural bridging")
        console.print("  • Emotional depth enhancement")


@cli.command()
def interactive():
    """Interactive prompt builder"""
    
    console.print("[bold cyan]Sora AI Interactive Prompt Builder[/bold cyan]\n")
    
    subject = click.prompt("Subject (required)")
    action = click.prompt("Action (optional)", default="", show_default=False)
    setting = click.prompt("Setting (optional)", default="", show_default=False)
    
    console.print("\n[yellow]Camera Options:[/yellow]")
    for i, cm in enumerate(CameraMovement, 1):
        console.print(f"{i}. {cm.value}")
    camera_choice = click.prompt("Camera movement (number or 0 for none)", type=int, default=0)
    
    console.print("\n[yellow]Style Options:[/yellow]")
    for i, s in enumerate(Style, 1):
        console.print(f"{i}. {s.value}")
    style_choice = click.prompt("Style (number or 0 for none)", type=int, default=0)
    
    mood = click.prompt("Mood (optional)", default="", show_default=False)
    
    generator = SoraPromptGenerator()
    
    elements = PromptElements(
        subject=subject,
        action=action if action else None,
        setting=setting if setting else None,
        camera_movement=list(CameraMovement)[camera_choice-1] if camera_choice > 0 else None,
        style=list(Style)[style_choice-1] if style_choice > 0 else None,
        mood=mood if mood else None
    )
    
    prompt = generator.generate(elements)
    
    console.print("\n")
    console.print(Panel(prompt, title="Your Generated Prompt", border_style="green"))
    
    if click.confirm("\nGenerate variations?"):
        count = click.prompt("How many variations?", type=int, default=3)
        variations = generator.generate_variations(elements, count)
        console.print("\n[bold]Variations:[/bold]")
        for i, var in enumerate(variations, 1):
            console.print(f"[cyan]{i}.[/cyan] {var}")
    
    if click.confirm("\nOptimize this prompt for better acceptance?"):
        optimizer = PromptOptimizer()
        framing_system = ContextFramingSystem()
        
        # Optimize the prompt
        result = optimizer.optimize(prompt)
        framing_result = framing_system.apply_framing(result.optimized_prompt)
        
        console.print("\n[bold green]Optimized Version:[/bold green]")
        console.print(Panel(framing_result["framed"], border_style="green"))
        console.print(f"Success likelihood: {framing_result['expected_success_rate']:.1%}")


if __name__ == "__main__":
    cli()