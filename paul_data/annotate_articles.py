import csv

input_file = 'paul_data/articles_102_205.csv'
output_file = 'paul_data/articles_102_205.csv'

# Sentiment assignment function
def assign_emotion(title, description, topic):
    s = (title + ' ' + description).lower()
    # Heuristic: Negative if mentions populism as threat, climate inaction, scandals, conflict, opposition, criticism
    negative_words = [
        'conflict', 'scandal', 'back on', 'complicating', 'temper tantrum', 'outrage', 'critical', 'apologized',
        'deficit', 'failure', 'halting', 'negative', 'attack', 'conservative', 'controversy', 'exposed', 'resigned',
        'blowback', 'failed', 'opposed', 'fiasco', 'problem', 'temper', 'fraud', 'fraudulent', 'sorry', 'disappointed',
        'canceled', 'pulls', 'shut down', 'backfires', 'caves', 'debate', 'tension', 'tariff', 'trade war', 'extra import tax',
        'not sorry', 'refuses to apologize', 'slams', 'drama', 'insult', 'emotional', 'pushed',
        'negative', 'questions', 'resigned', 'crisis', 'hostile', 'cuts', 'undermined'
    ]
    positive_words = [
        'success', 'win', 'super pumped', 'chief of staff', 'funding', 'relief', 'nation-building', 'achievement',
        'optimistic', 'support', 'pumped', 'praises', 'breakthrough', 'progress', 'pitches', 'best ever',
        'double', 'ambitious', 'positive', 'reliable', 'leader', 'appoint', 'generational', 'goal', 'strong', 'constructive',
        'agreement', 'deal', 'recognize', 'announce', 'hope', 'endorse', 'applause', 'living list'
    ]
    # Manual rules for high-precision headlines first
    if 'turning his back on climate' in s or 'illusion of control' in s:
        return 'negative'
    if 'apologized for anti-tariff' in s or 'conflict' in s or 'blowback' in s:
        return 'negative'
    if 'super pumped' in s or 'leadership' in topic.lower():
        return 'positive'
    # Wordlist-based heuristics
    if any(neg in s for neg in negative_words):
        return 'negative'
    if any(pos in s for pos in positive_words):
        return 'positive'
    # If about external dispute (e.g. US trade), neutral unless clearly negative/positive about Carney
    if topic in ["Trade Disputes", "International Relations"]:
        return 'neutral'
    # If about National Development or Budget, check for problem or praise
    if topic in ["Federal Budget", "National Development"]:
        if any(neg in s for neg in negative_words):
            return 'negative'
        if any(pos in s for pos in positive_words):
            return 'positive'
        return 'neutral'
    # Most Political Commentary is neutral unless headline is praise or attack
    return 'neutral'

rows = []
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    # Enforce correct header ordering (manual for clarity)
    correct_header = [
        'publishedAt', 'title', 'description', 'url', 'source_name', 'topic', 'emotion'
    ]
    rows.append(correct_header)
    for row in reader:
        # Defensive: flatten row and trim
        clean = [field.strip() for field in row]
        # Sometimes source_name is at the end -- if row[-1] is a known source name (website), move to 5
        # url check: should be index 3 and start with http(s) or www
        if len(clean) > 7:
            # assume surplus columns merged to description (for older versions)
            urlidx = None
            for idx, val in enumerate(clean):
                if val.startswith('http') or val.startswith('www.'):
                    urlidx = idx
                    break
            # publishedAt, title, description (join all between 2 and url-1), url, source_name, topic, emotion
            publishedAt = clean[0] if len(clean) > 0 else ''
            title = clean[1] if len(clean) > 1 else ''
            # description: join everything from index 2 up to urlidx
            description = ', '.join(clean[2:urlidx]) if urlidx and urlidx > 2 else ''
            url = clean[urlidx] if urlidx is not None else ''
            # source_name: next field
            source_name = clean[urlidx+1] if urlidx is not None and len(clean) > urlidx+1 else ''
            topic = clean[urlidx+2] if urlidx is not None and len(clean) > urlidx+2 else ''
            emotion = clean[urlidx+3] if urlidx is not None and len(clean) > urlidx+3 else ''
            norm = [publishedAt, title, description, url, source_name, topic, emotion]
        else:
            # If correct length, keep as is, otherwise pad or trim
            norm = (clean + ['']*7)[:7]
        rows.append(norm)
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
print('CSV normalized to 7 columns with correct ordering.')
