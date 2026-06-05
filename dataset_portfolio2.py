import pandas as pd
import random

# 1. Siapkan komponen kalimat untuk digabungkan secara acak
positive_templates = [
    ("The sound quality", "is absolutely amazing", "and crystal clear.", "Joy"),
    ("The battery life", "is incredible", "and lasts for days without charging.", "Joy"),
    ("The mobile app", "is super intuitive", "and very easy to configure.", "Joy"),
    ("The build quality", "feels premium", "and extremely sturdy in hand.", "Joy"),
    ("The delivery speed", "was lightning fast,", "arrived way ahead of schedule.", "Joy"),
    ("The customer support", "was extremely helpful", "and resolved my issue instantly.", "Joy"),
    ("The noise cancellation", "works like magic,", "it completely blocks out everything.", "Joy"),
    ("The design", "is sleek and beautiful,", "definitely worth every single penny.", "Joy"),
    ("The bluetooth connection", "is rock solid", "with zero latency or drops.", "Joy"),
    ("This product", "exceeded my expectations", "and improved my daily workflow.", "Joy")
]

negative_templates = [
    ("The battery", "dies after only 2 hours", "of very light usage. Terrible.", "Anger"),
    ("The screen", "arrived completely cracked", "and scratched. Very disappointed.", "Sadness"),
    ("The companion app", "keeps crashing constantly", "every time I try to open it.", "Anger"),
    ("The material", "feels cheap and plasticky,", "definitely not worth the premium price.", "Sadness"),
    ("The delivery", "took almost three weeks", "and the packaging was badly damaged.", "Anger"),
    ("The customer service", "was completely useless", "and ignored my refund request.", "Anger"),
    ("The touch controls", "are totally unresponsive", "and frustrating to use.", "Anger"),
    ("The audio output", "sounds very muddy", "and has a constant static hiss.", "Sadness"),
    ("The charging port", "stopped working entirely", "after just three days of use.", "Sadness"),
    ("The setup process", "is extremely confusing", "due to a poorly translated manual.", "Anger")
]

neutral_templates = [
    ("The product", "is okay for the price,", "nothing special but it works.", "Sadness"),
    ("The design", "is quite standard,", "neither good nor bad honestly.", "Joy"),
    ("The battery", "lasts around 5 hours,", "which is pretty average nowadays.", "Sadness"),
    ("The shipping", "was slightly delayed", "but it arrived safely eventually.", "Sadness"),
    ("The sound", "is decent enough for casual listening,", "but lacks deep bass.", "Sadness"),
    ("It works", "exactly as described", "but doesn't have any extra features.", "Joy"),
    ("The size", "is a bit smaller than expected,", "but still usable for me.", "Sadness"),
    ("The material", "is just normal plastic,", "feels okay given the low price.", "Sadness"),
    ("The connection", "drops once in a while,", "but reconnects quickly by itself.", "Sadness"),
    ("The packaging", "was minimal", "but it kept the item safe from scratches.", "Joy")
]

# 2. Loop untuk menghasilkan 1000 data bervariasi
reviews = []
sentiments = []
emotions = []

# Kita bagi rata: ~334 positif, ~333 negatif, ~333 netral
for i in range(1000):
    if i % 3 == 0:
        # Ambil template positif secara acak
        comp, adj, conclusion, emo = random.choice(positive_templates)
        # Beri sedikit variasi tambahan acak di akhir kalimat agar tidak kembar identik
        filler = random.choice(["Highly recommended!", "Love it so much.", "Will buy again.", "Great job!"])
        review_text = f"{comp} {adj} {conclusion} {filler}"
        sentiment_label = "Positive"
    elif i % 3 == 1:
        # Ambil template negatif secara acak
        comp, adj, conclusion, emo = random.choice(negative_templates)
        filler = random.choice(["Worst purchase ever.", "Please avoid this.", "Extremely frustrated.", "Waste of money."])
        review_text = f"{comp} {adj} {conclusion} {filler}"
        sentiment_label = "Negative"
    else:
        # Ambil template netral secara acak
        comp, adj, conclusion, emo = random.choice(neutral_templates)
        filler = random.choice(["Just standard.", "It's acceptable.", "Nothing to hype about.", "Fair enough."])
        review_text = f"{comp} {adj} {conclusion} {filler}"
        sentiment_label = "Neutral"
        
    reviews.append(review_text)
    sentiments.append(sentiment_label)
    emotions.append(emo)

# 3. Simpan ke DataFrame dan export ke CSV
df_1000 = pd.DataFrame({
    'Review_Text': reviews,
    'Sentiment': sentiments,
    'Emotion': emotions
})

# Mengacak urutan baris agar datanya terlihat natural (tidak berurutan pos, neg, neu)
df_1000 = df_1000.sample(frac=1).reset_index(drop=True)

df_1000.to_csv('customer_feedback1.csv', index=False)

print(f"📊 Total data yang digenerate: {len(df_1000)} baris.")
print("✅ File 'customer_feedback.csv' dengan 1.000 kalimat sukses dibuat!")