# %%
text = """
a: 3
b: 4
c: 5
"""
# %%
transforms = {
    'a': lambda s: sum(s),
    'b': lambda s: s * 3,
    'c': lambda s: s * 3,
}
default = lambda s: s


# %%
lines = text.strip().splitlines()
lines[:5]

# %%
fields = dict([line.split(':', 1) for line in lines])
fields

# %% 
final_data = {k: transforms.get(k, default)(v) for k, v in fields.items()}

# %%
for para in paragraphs:
    text = para.text.strip()
    
    if text.startswith('Type:'):
        if report_data['type']:
            report_data = {'type': '', 'scholar': '', 'date': '', 'topic': '', 'content': ''}
        report_data['type'] = text.replace('Type:', '').strip()
        current_section = 'content'
    elif text.startswith('Scholar:'):
        report_data['scholar'] = text.replace('Scholar:', '').strip()
    elif text.startswith('Date:'):
        report_data['date'] = text.replace('Date:', '').strip()
    elif text.startswith('Topic:'):
        report_data['topic'] = text.replace('Topic:', '').strip()
    elif text.startswith('Content:'):
        report_data['content'] = text.replace('Content:', '').strip()
        current_section = 'content'
    elif current_section == 'content':
        report_data['content'] += '\n' + text