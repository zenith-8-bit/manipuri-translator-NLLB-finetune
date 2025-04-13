import re

# Read input from file
with open('output2.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pairs = []
current_line = ''
skip_next = False  # To handle multi-line skip patterns

# Patterns to skip (including abbreviations and section headers)
skip_patterns = [
    r'^Page \d+$',
    r'^[IVXLCDM]+$',
    r'^\s*(v|adj|adv|nom)\.\s+',
    r'^\s*(Phr|idiom|Abbreviations|In the transliteration|Vowel signs)',
    r'^\s*\d+\.\d+\s+[\w\.]+'  # Skip numbered entries like "01.0 ka.ng2"
]

for line in text.split('\n'):
    line = line.strip()
    
    # Skip empty lines
    if not line:
        continue
        
    # Check if we should skip this line based on patterns
    skip = False
    for pattern in skip_patterns:
        if re.search(pattern, line, re.IGNORECASE):
            skip = True
            break
            
    if skip:
        skip_next = True  # Skip subsequent lines until next valid entry
        continue
        
    # Reset skip flag if we passed a skipped section
    if skip_next:
        if ',,,' not in line:
            continue
        else:
            skip_next = False

    # Handle multi-line entries
    if current_line:
        current_line += ' ' + line
    else:
        current_line = line

    # Check if we have a complete pair
    if ',,,' in current_line:
        # Split into Manipuri and English parts
        parts = re.split(r'\s*,,,\s*', current_line, 1)
        if len(parts) == 2:
            manipuri, english = parts[0].strip(), parts[1].strip()
            
            manipuri = re.sub(r'\b(adj|v|n|adv)\.\s*', '', manipuri)  # Remove grammatical markers
            manipuri = re.sub(r'[-\']', '', manipuri)  # Remove hyphens and apostrophes for consistency
            manipuri = re.sub(r'\b(adj|v|n|adv)\.\s*', '', manipuri)
            
            # Add valid pairs (both parts non-empty)
            if manipuri and english:
                pairs.append(f"{manipuri} ,,, {english}")
                
        current_line = ''

# Save results
with open('extr.txt', 'w', encoding='utf-8') as f:
    f.write("Manipuri ,,, English\n")
    f.write("\n".join(sorted(list(set(pairs)))))

print(f"Successfully extracted {len(pairs)} Manipuri-English pairs")