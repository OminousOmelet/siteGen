from markdown_blocks import markdown_to_blocks, block_to_block_type

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        