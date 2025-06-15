# FIXED Cell 5 - Copy this into Colab Cell 5
# This should run continuously, not finish in 0ms

print("🚀 Starting the processor...")
print("💡 This cell should run continuously, not finish immediately")

# Check if processor exists
if 'processor' not in globals():
    print("❌ Processor not found - run Cell 4 first")
else:
    print("✅ Processor found, starting...")
    
    # Start with shorter duration for testing
    import threading
    import time
    
    def run_processor():
        """Run processor in a way that shows output"""
        processor.running = True
        start_time = time.time()
        duration = 300  # 5 minutes for testing
        
        print(f"🚀 Processor started for {duration//60} minutes")
        print("⏱️ Checking for commands every 3 seconds...")
        
        while processor.running and (time.time() - start_time < duration):
            try:
                commands = processor.get_commands()
                
                if commands:
                    print(f"📨 Found {len(commands)} commands to process")
                    for cmd in commands:
                        processor.process_command(cmd)
                        if not processor.running:
                            break
                else:
                    elapsed = int(time.time() - start_time)
                    print(f"⏳ No commands... running {elapsed}s (processed: {processor.stats['processed']}, errors: {processor.stats['errors']})")
                
                time.sleep(3)
                
            except KeyboardInterrupt:
                print("🛑 Stopped by user")
                processor.running = False
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(5)
        
        print("🛑 Processor stopped")
        print(f"📊 Final stats: {processor.stats['processed']} processed, {processor.stats['errors']} errors")
    
    # Run processor
    run_processor()