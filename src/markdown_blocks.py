from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

# converts single markdown string into list of markdown blocks
def markdown_to_blocks(markdown):
    if markdown == "":
        return []
    blocks = markdown.strip().split("\n\n")
    stripped = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        stripped.append(block)
    return stripped

# returns the blocktype of a given markdown block
def block_to_block_type(block):
    if re.match(r"#{1,6} ", block[:8]) != None:
        return BlockType.HEADING
    if re.match(r"`{3}.+`{3}", block, re.DOTALL) != None:
        return BlockType.CODE

    lines = block.split('\n')
    block_type = check_lines(lines, r"> ", BlockType.QUOTE)
    if block_type == BlockType.QUOTE:
        return block_type
    block_type = check_lines(lines, r"- ", BlockType.ULIST)
    if block_type == BlockType.ULIST:
        return block_type
    block_type = check_lines(lines, r"\d\. ", BlockType.OLIST)
    return block_type

# helper function
def check_lines(lines, regex, block_type):
    for line in lines:
        if re.match(regex, line[:3]) == None:
            return BlockType.PARAGRAPH
    return block_type