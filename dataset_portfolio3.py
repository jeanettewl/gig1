import os
import pandas as pd

def export_telemetry_to_csv():
    """
    Data Engineering Pipeline - Phase 1: Ingestion
    Converts raw translated NLP telemetry data dictionary into a structured CSV file.
    """
    
    # Raw telemetry dictionary with 107 records (English translated dataset)
    telemetry_data = {
        "text_id": ['TXT-001', 'TXT-002', 'TXT-003', 'TXT-004', 'TXT-005', 'TXT-006', 'TXT-007', 'TXT-008', 'TXT-009', 'TXT-010', 'TXT-011', 'TXT-012', 'TXT-013', 'TXT-014', 'TXT-015', 'TXT-016', 'TXT-017', 'TXT-018', 'TXT-019', 'TXT-020', 'TXT-021', 'TXT-022', 'TXT-023', 'TXT-024', 'TXT-025', 'TXT-026', 'TXT-027', 'TXT-028', 'TXT-029', 'TXT-030', 'TXT-031', 'TXT-032', 'TXT-033', 'TXT-034', 'TXT-035', 'TXT-036', 'TXT-037', 'TXT-038', 'TXT-039', 'TXT-040', 'TXT-041', 'TXT-042', 'TXT-043', 'TXT-044', 'TXT-045', 'TXT-046', 'TXT-047', 'TXT-048', 'TXT-049', 'TXT-050', 'TXT-051', 'TXT-052', 'TXT-053', 'TXT-054', 'TXT-055', 'TXT-056', 'TXT-057', 'TXT-058', 'TXT-059', 'TXT-060', 'TXT-061', 'TXT-062', 'TXT-063', 'TXT-064', 'TXT-065', 'TXT-066', 'TXT-067', 'TXT-068', 'TXT-069', 'TXT-070', 'TXT-071', 'TXT-072', 'TXT-073', 'TXT-074', 'TXT-075', 'TXT-076', 'TXT-077', 'TXT-078', 'TXT-079', 'TXT-080', 'TXT-081', 'TXT-082', 'TXT-083', 'TXT-084', 'TXT-085', 'TXT-086', 'TXT-087', 'TXT-088', 'TXT-089', 'TXT-090', 'TXT-091', 'TXT-092', 'TXT-093', 'TXT-094', 'TXT-095', 'TXT-096', 'TXT-097', 'TXT-098', 'TXT-099', 'TXT-100', 'TXT-101', 'TXT-102', 'TXT-103', 'TXT-104', 'TXT-105', 'TXT-106', 'TXT-107'],
        "timestamp": ['2026-06-01 09:15:22', '2026-06-01 10:02:11', '2026-06-01 11:45:00', '2026-06-02 14:20:05', '2026-06-02 16:33:40', '2026-06-03 08:12:19', '2026-06-03 13:05:55', '2026-06-03 18:29:43', '2026-06-03 19:46:17', '2026-06-03 23:23:03', '2026-06-04 03:22:20', '2026-06-04 06:17:16', '2026-06-04 07:44:46', '2026-06-04 11:15:25', '2026-06-04 15:46:16', '2026-06-04 17:34:11', '2026-06-04 20:30:16', '2026-06-04 22:50:57', '2026-06-05 02:40:48', '2026-06-05 06:56:56', '2026-06-05 09:47:04', '2026-06-05 11:43:03', '2026-06-05 16:16:37', '2026-06-05 20:41:01', '2026-06-06 00:36:15', '2026-06-06 01:46:14', '2026-06-06 03:00:30', '2026-06-06 06:47:04', '2026-06-06 11:21:44', '2026-06-06 13:42:04', '2026-06-06 15:19:47', '2026-06-06 16:44:03', '2026-06-06 21:05:15', '2026-06-07 00:26:07', '2026-06-07 03:03:07', '2026-06-07 06:18:20', '2026-06-07 09:37:37', '2026-06-07 10:55:04', '2026-06-07 14:04:47', '2026-06-07 18:03:00', '2026-06-07 20:33:43', '2026-06-07 23:36:31', '2026-06-08 04:22:24', '2026-06-08 09:16:03', '2026-06-08 11:03:00', '2026-06-08 14:43:40', '2026-06-08 17:59:15', '2026-06-08 19:43:08', '2026-06-08 22:52:19', '2026-06-09 01:21:02', '2026-06-09 04:54:19', '2026-06-09 07:11:01', '2026-06-09 10:14:15', '2026-06-09 14:38:32', '2026-06-09 19:10:04', '2026-06-09 21:28:47', '2026-06-10 01:28:09', '2026-06-10 03:51:39', '2026-06-10 07:46:17', '2026-06-10 10:29:41', '2026-06-10 14:52:03', '2026-06-10 16:35:48', '2026-06-10 21:29:44', '2026-06-11 02:26:08', '2026-06-11 05:43:54', '2026-06-11 07:33:14', '2026-06-11 09:20:20', '2026-06-11 10:35:25', '2026-06-11 12:44:49', '2026-06-11 17:28:20', '2026-06-11 19:54:13', '2026-06-11 23:49:15', '2026-06-12 02:40:08', '2026-06-12 04:08:24', '2026-06-12 07:54:15', '2026-06-12 11:25:21', '2026-06-12 14:41:43', '2026-06-12 18:28:05', '2026-06-12 21:07:05', '2026-06-12 23:25:40', '2026-06-13 04:19:11', '2026-06-13 09:07:04', '2026-06-13 13:46:27', '2026-06-13 14:49:57', '2026-06-13 19:16:51', '2026-06-13 20:30:15', '2026-06-13 23:54:40', '2026-06-14 01:21:45', '2026-06-14 02:29:32', '2026-06-14 05:22:20', '2026-06-14 08:31:05', '2026-06-14 09:59:14', '2026-06-14 14:52:12', '2026-06-14 16:48:47', '2026-06-14 21:13:08', '2026-06-15 01:16:34', '2026-06-15 05:14:46', '2026-06-15 06:46:17', '2026-06-15 11:45:01', '2026-06-15 13:48:19', '2026-06-15 18:41:00', '2026-06-15 21:19:54', '2026-06-16 00:26:07', '2026-06-16 02:46:42', '2026-06-16 06:50:52', '2026-06-16 11:40:48', '2026-06-16 13:20:07'],
        "user_input": [
            "I feel extremely anxious and panicked about this final semester exam.",
            "This app is very helpful for me to organize my schedule neatly. Thank you!",
            "Please, I feel so overwhelmed and don't know what else to do right now.",
            "The system keeps crashing, I'm so frustrated while chasing a deadline!",
            "Overall, the model performance is quite stable and consistent.",
            "I feel lost, like there's no way out of this difficult situation.",
            "Wow amazing! The prediction is very accurate and fast.",
            "I am incredibly nervous ahead of the comprehensive exam defense next week.",
            "I really hate it when group members disappear without a trace right before a deadline.",
            "I am afraid of disappointing my parents because my GPA dropped this semester.",
            "Deeply disappointed with the results of this experiment, I feel like giving up.",
            "Crying alone in my room because I feel crushed by the expectations around me.",
            "Getting a sudden revision request with only a few hours deadline is completely inhumane!",
            "The technical coordination meeting will start tomorrow morning at 09:00 AM.",
            "Terrified of making the wrong decision for the continuation of this hybrid research.",
            "Getting a sudden revision request with only a few hours deadline is completely inhumane!",
            "Wow amazing! The prediction is very accurate and fast.",
            "It makes me furious to see someone else take credit for my hard work.",
            "I already told you not to change the .env configuration file without prior coordination!",
            "The IndoBERT model acts as a contextual feature extractor for the input text.",
            "I really hate it when group members disappear without a trace right before a deadline.",
            "Worried about losing my research data because the external hard drive is unreadable.",
            "The technical coordination meeting will start tomorrow morning at 09:00 AM.",
            "Alhamdulillah, my research paper is officially accepted and In Press at IJCCS UGM!",
            "I've been feeling directionless and unmotivated to do anything for a week now.",
            "Sad to see months of hard work rejected directly without a clear review.",
            "Suddenly my heart is racing so fast, feeling terrified for absolutely no reason.",
            "So happy because the accuracy of the IndoBERT + Random Forest model jumped sharply!",
            "Lost the motivation to write, can only stare at a blank screen for hours.",
            "Extremely annoyed with the unstable campus internet connection today.",
            "I am incredibly nervous ahead of the comprehensive exam defense next week.",
            "Completely panicking because the server suddenly went down 5 minutes before the presentation.",
            "It feels so unfair that the grading criteria were changed unilaterally at the end of the semester.",
            "Getting positive feedback from users restores my motivation completely.",
            "Sad because a minor misunderstanding ruined a long-standing friendship.",
            "Dataset cleaning is performed by removing null values using Pandas.",
            "The training process for the Random Forest model takes about ten minutes.",
            "The technical coordination meeting will start tomorrow morning at 09:00 AM.",
            "So happy because the accuracy of the IndoBERT + Random Forest model jumped sharply!",
            "I really hate it when group members disappear without a trace right before a deadline.",
            "What if this AI model fails to detect a crisis situation when the system is deployed?",
            "I am incredibly nervous ahead of the comprehensive exam defense next week.",
            "Sometimes I feel lonely amidst the crowded campus, nobody truly understands.",
            "Suddenly my heart is racing so fast, feeling terrified for absolutely no reason.",
            "The technical coordination meeting will start tomorrow morning at 09:00 AM.",
            "I am just so tired of pretending everything is fine in front of other people.",
            "Suddenly my heart is racing so fast, feeling terrified for absolutely no reason.",
            "I am afraid of disappointing my parents because my GPA dropped this semester.",
            "So happy because the accuracy of the IndoBERT + Random Forest model jumped sharply!",
            "This system is incredibly slow and clunky, a complete waste of my time!",
            "I am deeply anxious thinking about my thesis advising session tomorrow morning.",
            "Why does this code suddenly error right when I'm about to show it to the professor?! So frustrating!",
            "Sad to see months of hard work rejected directly without a clear review.",
            "I've been feeling directionless and unmotivated to do anything for a week now.",
            "Why is this API documentation such a mess? It's highly inconvenient for developers!",
            "Today was so productive, managed to complete revisions for both chapter 4 and chapter 5.",
            "Extremely annoyed with the unstable campus internet connection today.",
            "So happy because the accuracy of the IndoBERT + Random Forest model jumped sharply!",
            "Alhamdulillah, my research paper is officially accepted and In Press at IJCCS UGM!",
            "So happy because the accuracy of the IndoBERT + Random Forest model jumped sharply!",
            "I really hate it when group members disappear without a trace right before a deadline.",
            "The training process for the Random Forest model takes about ten minutes.",
            "Sad to see months of hard work rejected directly without a clear review.",
            "I really hate it when group members disappear without a trace right before a deadline.",
            "Why does this code suddenly error right when I'm about to show it to the professor?! So frustrating!",
            "I feel lost, as if every exit is closed for this particular problem.",
            "Extremely annoyed with the unstable campus internet connection today.",
            "So happy because the accuracy of the IndoBERT + Random Forest model jumped sharply!",
            "Telemetry log data is saved periodically in CSV format on the local system.",
            "I am deeply anxious thinking about my thesis advising session tomorrow morning.",
            "I am incredibly nervous ahead of the comprehensive exam defense next week.",
            "This system is incredibly slow and clunky, a complete waste of my time!",
            "Getting a sudden revision request with only a few hours deadline is completely inhumane!",
            "Missing the relaxing days without a mounting pile of academic stress.",
            "Please download the dashboard configuration file through the link provided in the sidebar.",
            "So happy because the accuracy of the IndoBERT + Random Forest model jumped sharply!",
            "Worried about losing my research data because the external hard drive is unreadable.",
            "This system is incredibly slow and clunky, a complete waste of my time!",
            "I am deeply anxious thinking about my thesis advising session tomorrow morning.",
            "The vibe of this room makes me feel highly uncomfortable and somewhat on edge.",
            "So happy because the accuracy of the IndoBERT + Random Forest model jumped sharply!",
            "Suddenly my heart is racing so fast, feeling terrified for absolutely no reason.",
            "Crying alone in my room because I feel crushed by the expectations around me.",
            "Please download the dashboard configuration file through the link provided in the sidebar.",
            "Worried about losing my research data because the external hard drive is unreadable.",
            "Don't just accuse this model of plagiarism before reading its architectural documentation!",
            "I am incredibly nervous ahead of the comprehensive exam defense next week.",
            "Extremely annoyed with the unstable campus internet connection today.",
            "I really hate it when group members disappear without a trace right before a deadline.",
            "Crying alone in my room because I feel crushed by the expectations around me.",
            "Awesome, getting to relax for a bit today while enjoying a warm cup of coffee.",
            "The technical coordination meeting will start tomorrow morning at 09:00 AM.",
            "The technical coordination meeting will start tomorrow morning at 09:00 AM.",
            "Deeply disappointed with the results of this experiment, I feel like giving up.",
            "I really hate it when group members disappear without a trace right before a deadline.",
            "Don't just accuse this model of plagiarism before reading its architectural documentation!",
            "The technical coordination meeting will start tomorrow morning at 09:00 AM.",
            "So happy because the accuracy of the IndoBERT + Random Forest model jumped sharply!",
            "Getting positive feedback from users restores my motivation completely.",
            "I am afraid of disappointing my parents because my GPA dropped this semester.",
            "The technical coordination meeting will start tomorrow morning at 09:00 AM.",
            "I am incredibly nervous ahead of the comprehensive exam defense next week.",
            "Sad because a minor misunderstanding ruined a long-standing friendship.",
            "I am deeply anxious thinking about my thesis advising session tomorrow morning.",
            "I feel lost, as if every exit is closed for this particular problem.",
            "Completely panicking because the server suddenly went down 5 minutes before the presentation.",
            "Dataset cleaning is performed by removing null values using Pandas."
        ],
        "predicted_emotion": ['Fear', 'Joy', 'Sadness', 'Anger', 'Neutral', 'Sadness', 'Joy', 'Fear', 'Anger', 'Fear', 'Sadness', 'Sadness', 'Anger', 'Neutral', 'Fear', 'Anger', 'Joy', 'Anger', 'Anger', 'Neutral', 'Anger', 'Fear', 'Neutral', 'Joy', 'Sadness', 'Sadness', 'Fear', 'Joy', 'Sadness', 'Anger', 'Fear', 'Fear', 'Anger', 'Joy', 'Sadness', 'Neutral', 'Neutral', 'Neutral', 'Joy', 'Anger', 'Fear', 'Fear', 'Sadness', 'Fear', 'Neutral', 'Sadness', 'Fear', 'Fear', 'Joy', 'Anger', 'Fear', 'Anger', 'Sadness', 'Sadness', 'Anger', 'Joy', 'Anger', 'Joy', 'Joy', 'Joy', 'Anger', 'Neutral', 'Sadness', 'Anger', 'Anger', 'Sadness', 'Anger', 'Joy', 'Neutral', 'Fear', 'Fear', 'Anger', 'Anger', 'Sadness', 'Neutral', 'Joy', 'Fear', 'Anger', 'Fear', 'Fear', 'Joy', 'Fear', 'Sadness', 'Neutral', 'Fear', 'Anger', 'Fear', 'Anger', 'Anger', 'Sadness', 'Joy', 'Neutral', 'Neutral', 'Sadness', 'Anger', 'Anger', 'Neutral', 'Joy', 'Joy', 'Fear', 'Neutral', 'Fear', 'Sadness', 'Fear', 'Sadness', 'Fear', 'Neutral'],
        "crisis_level": ['High', 'Low', 'High', 'Medium', 'Low', 'High', 'Low', 'Medium', 'High', 'Medium', 'Medium', 'High', 'High', 'Low', 'Low', 'High', 'Low', 'High', 'Medium', 'Low', 'High', 'Medium', 'Low', 'Low', 'High', 'Medium', 'High', 'Low', 'Medium', 'Low', 'Medium', 'High', 'Medium', 'Low', 'Medium', 'Low', 'Low', 'Low', 'Low', 'High', 'Medium', 'Medium', 'Medium', 'High', 'Low', 'High', 'High', 'Medium', 'Low', 'Medium', 'High', 'Medium', 'Medium', 'High', 'Medium', 'Low', 'Low', 'Low', 'Low', 'Low', 'High', 'Low', 'Medium', 'High', 'Medium', 'High', 'Low', 'Low', 'Low', 'High', 'Medium', 'Medium', 'High', 'Low', 'Low', 'Low', 'Medium', 'Medium', 'High', 'Low', 'Low', 'High', 'High', 'Low', 'Medium', 'Medium', 'Medium', 'Low', 'High', 'High', 'Low', 'Low', 'Low', 'Medium', 'High', 'Medium', 'Low', 'Low', 'Low', 'Medium', 'Low', 'Medium', 'Medium', 'High', 'High', 'High', 'Low'],
        "confidence_score": [0.94, 0.89, 0.97, 0.85, 0.78, 0.95, 0.91, 0.83, 0.88, 0.96, 0.98, 0.93, 0.93, 0.75, 0.97, 0.91, 0.85, 0.97, 0.92, 0.76, 0.96, 0.9, 0.72, 0.83, 0.93, 0.97, 0.88, 0.87, 0.96, 0.89, 0.88, 0.84, 0.83, 0.96, 0.85, 0.77, 0.76, 0.71, 0.96, 0.94, 0.9, 0.83, 0.87, 0.86, 0.84, 0.98, 0.83, 0.82, 0.83, 0.94, 0.89, 0.87, 0.85, 0.85, 0.86, 0.91, 0.97, 0.88, 0.99, 0.84, 0.98, 0.73, 0.86, 0.92, 0.89, 0.92, 0.9, 0.96, 0.83, 0.96, 0.89, 0.84, 0.94, 0.88, 0.72, 0.99, 0.97, 0.85, 0.95, 0.96, 0.84, 0.9, 0.97, 0.86, 0.89, 0.96, 0.95, 0.97, 0.97, 0.93, 0.98, 0.7, 0.8, 0.89, 0.93, 0.98, 0.86, 0.88, 0.89, 0.87, 0.86, 0.98, 0.85, 0.83, 0.93, 0.91, 0.82]
    }
    
    # 1. Convert dictionary into Pandas DataFrame
    df = pd.DataFrame(telemetry_data)
    
    # 2. Setup target directory safely
    output_folder = "data"
    os.makedirs(output_folder, exist_ok=True)
    
    # 3. Export to structured CSV file
    file_name = "sample_crisis_emotions.csv"
    full_path = os.path.join(output_folder, file_name)
    df.to_csv(full_path, index=False)
    
    # 4. Success Telemetry Log for Terminal View
    print("="*65)
    print(f" 🛡️  DATA PIPELINE INGESTION LOG")
    print(f" Status      : SUCCESS -> Export completed successfully.")
    print(f" Output Path : {full_path}")
    print(f" Structure   : {df.shape[0]} samples ingested | {df.shape[1]} metrics logged.")
    print("="*65)

if __name__ == "__main__":
    export_telemetry_to_csv()