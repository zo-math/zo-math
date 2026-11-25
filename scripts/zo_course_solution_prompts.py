"""Reuse the rendered task prompt beside its matching worked solution."""
from copy import deepcopy
import re
from urllib.parse import quote, unquote

from bs4 import BeautifulSoup


def task_for_answer(answer, tasks, document):
    task = tasks.get(answer.get('data-zo-task'))
    if task is not None:
        return task
    # A legacy solution uses the return anchor in place of a task key.
    backlink = answer.select_one('.answer-link a[href^="#"]')
    if backlink:
        task = document.find(id=unquote(backlink['href'][1:]))
        if task and task.get('data-zo-type') == 'task':
            return task
    raise ValueError(f'Solution has no source task: {answer["id"]}')


def copy_prompt(task, answer_id, document):
    region = task.find(class_='reading-region', recursive=False) or task
    prompt = document.new_tag('details', attrs={'class': 'zo-solution-prompt'})
    heading = document.new_tag('summary', attrs={'class': 'zo-solution-prompt-label'})
    for state, label in (('show', 'Hiện đề bài'), ('hide', 'Ẩn đề bài')):
        label_span = document.new_tag('span', attrs={'class': f'zo-solution-prompt-{state}'})
        label_span.string = label
        heading.append(label_span)
    prompt.append(heading)
    body = document.new_tag('div', attrs={'class': 'zo-solution-prompt-body'})
    for part in region.find_all(recursive=False):
        classes = part.get('class', [])
        if (part.name in {'h2', 'h3', 'h4', 'h5', 'h6'} or part.has_attr('data-reading-label')
                or 'answer-link' in classes or 'zo-learning-video' in classes
                or part.get('id', '').startswith('tieu-chi-')
                or part.select_one(':scope > .zo-task-title')):
            continue
        copy = deepcopy(part)
        if 'r1-transfer-conditional' in classes:
            copy['class'] = [name for name in classes if name not in {'zo-block', 'zo-block-gray'}]
        body.append(copy)
    if not body.contents:
        raise ValueError(f'Source task has no prompt content: {task.get("id")}')
    prompt.append(body)

    # Namespace copied IDs and local ID references. The source task remains the
    # owner of canonical table identifiers and of links to its original anchors.
    ids = {node['id']: f'de-{answer_id}-{node["id"]}' for node in prompt.select('[id]')}
    for node in prompt.find_all():
        if node.has_attr('id'):
            node['id'] = ids[node['id']]
        node.attrs.pop('data-bbt', None)
        for attr in ('aria-controls', 'aria-describedby', 'aria-labelledby', 'headers', 'for'):
            if node.has_attr(attr):
                value = node[attr]
                tokens = value if isinstance(value, list) else value.split()
                node[attr] = ' '.join(ids.get(token, token) for token in tokens)
        for attr in ('href', 'xlink:href'):
            dest = node.get(attr, '')
            if dest.startswith('#') and (anchor := unquote(dest[1:])) in ids:
                node[attr] = '#' + quote(ids[anchor])
    return str(prompt)


def project_solution_prompts(text):
    if 'data-zo-solution-prompts="true"' not in text:
        return text
    from zo_course_site_sections import Locations

    document = BeautifulSoup(text, 'html.parser')
    solutions = document.select_one('#loi-giai[data-zo-solution-prompts="true"]')
    if solutions is None:
        raise ValueError('Solution prompt projection needs the declared solution view')
    answers = solutions.select('details.r1-solution[id]')
    tasks = {task['data-zo-task']: task for task in document.select('[data-zo-type="task"][data-zo-task]')}
    answer_offsets = Locations(text, {answer['id'] for answer in answers}).spans
    context_ids = {node['id'] for node in solutions.select('div.zo-solution-context[id]')}
    context_offsets = Locations(text, context_ids).spans if context_ids else {}
    changes = []
    for answer in answers:
        answer_id = answer['id']
        context_id = f'ngu-canh-{answer_id}'
        prompt = copy_prompt(task_for_answer(answer, tasks, document), answer_id, document)
        if context_id in context_offsets:
            start, end = context_offsets[context_id]
            changes.append((start, end, prompt))
            continue
        start, end = answer_offsets[answer_id]
        body = re.search(r'</summary>\s*<div class="zo-block-body">', text[start:end])
        if body is None:
            raise ValueError(f'Solution body missing: {answer_id}')
        offset = start + body.end()
        changes.append((offset, offset, f'<div class="zo-solution-context" id="{context_id}">{prompt}</div>'))
    for start, end, value in sorted(changes, reverse=True):
        text = text[:start] + value + text[end:]
    return text
