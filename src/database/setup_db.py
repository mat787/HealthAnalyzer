import os
import sqlite3
from src.utils.parser import load_all_health_data
from src.utils.utils import clean_data

XML_PATH = "../../eksport.xml"
DB_PATH = "health_data.db"

short_names = {
    # --- CIAŁO / PODSTAWOWE ---
    'HKQuantityTypeIdentifierHeight': 'height',
    'HKQuantityTypeIdentifierBodyMass': 'weight',
    'HKQuantityTypeIdentifierWaistCircumference': 'waist',
    'HKQuantityTypeIdentifierBodyFatPercentage': 'fat_pct',
    'Me': 'profile',

    # --- SERCE (HEART) ---
    'HKQuantityTypeIdentifierHeartRate': 'hr',
    'HKQuantityTypeIdentifierRestingHeartRate': 'rhr',
    'HKQuantityTypeIdentifierWalkingHeartRateAverage': 'hr_walk_avg',
    'HKQuantityTypeIdentifierHeartRateVariabilitySDNN': 'hrv',
    'HKQuantityTypeIdentifierHeartRateRecoveryOneMinute': 'hrr_1min',
    'HKCategoryTypeIdentifierHighHeartRateEvent': 'hr_high_event',
    'InstantaneousBeatsPerMinute': 'hr_instant',

    # --- AKTYWNOŚĆ / ENERGIA ---
    'HKQuantityTypeIdentifierStepCount': 'steps',
    'HKQuantityTypeIdentifierDistanceWalkingRunning': 'dist_walk',
    'HKQuantityTypeIdentifierDistanceCycling': 'dist_cycle',
    'HKQuantityTypeIdentifierBasalEnergyBurned': 'kcal_basal',
    'HKQuantityTypeIdentifierActiveEnergyBurned': 'kcal_active',
    'HKQuantityTypeIdentifierFlightsClimbed': 'flights',
    'HKQuantityTypeIdentifierAppleExerciseTime': 'exercise_min',
    'HKQuantityTypeIdentifierAppleStandTime': 'stand_min',
    'HKCategoryTypeIdentifierAppleStandHour': 'stand_hr',
    'HKQuantityTypeIdentifierPhysicalEffort': 'effort',
    'HKQuantityTypeIdentifierVO2Max': 'vo2max',
    'ActivitySummary': 'activity_summary',

    # --- MOBILNOŚĆ / CHÓD ---
    'HKQuantityTypeIdentifierWalkingSpeed': 'walk_speed',
    'HKQuantityTypeIdentifierWalkingStepLength': 'walk_step_len',
    'HKQuantityTypeIdentifierWalkingAsymmetryPercentage': 'walk_asym',
    'HKQuantityTypeIdentifierWalkingDoubleSupportPercentage': 'walk_dbl_supp',
    'HKQuantityTypeIdentifierStairAscentSpeed': 'stair_up_speed',
    'HKQuantityTypeIdentifierStairDescentSpeed': 'stair_down_speed',
    'HKQuantityTypeIdentifierAppleWalkingSteadiness': 'walk_steadiness',
    'HKQuantityTypeIdentifierSixMinuteWalkTestDistance': 'walk_6min',

    # --- ODDECH / POZIOMY ---
    'HKQuantityTypeIdentifierOxygenSaturation': 'spo2',
    'HKQuantityTypeIdentifierRespiratoryRate': 'resp_rate',

    # --- SEN ---
    'HKCategoryTypeIdentifierSleepAnalysis': 'sleep',
    'HKDataTypeSleepDurationGoal': 'sleep_goal',
    'HKQuantityTypeIdentifierAppleSleepingWristTemperature': 'wrist_temp',

    # --- ŚRODOWISKO / DŹWIĘK ---
    'HKQuantityTypeIdentifierEnvironmentalAudioExposure': 'audio_env',
    'HKQuantityTypeIdentifierHeadphoneAudioExposure': 'audio_hp',
    'HKQuantityTypeIdentifierEnvironmentalSoundReduction': 'sound_red',
    'HKCategoryTypeIdentifierAudioExposureEvent': 'audio_event',
    'HKCategoryTypeIdentifierHeadphoneAudioExposureEvent': 'audio_hp_event',
    'HKQuantityTypeIdentifierTimeInDaylight': 'daylight',

    # --- TRENINGI (WORKOUTS) ---
    'HKWorkoutActivityTypeWalking': 'workout_walking',
    'HKWorkoutActivityTypeCycling': 'workout_cycling',
    'HKWorkoutActivityTypePilates': 'workout_pilates',
    'HKWorkoutActivityTypeFunctionalStrengthTraining': 'workout_strength',
    'HKWorkoutActivityTypeTennis': 'workout_tennis',
    'HKWorkoutActivityTypeStairClimbing': 'workout_stairs',
    'HKWorkoutActivityTypeElliptical': 'workout_elliptical',
    'HKWorkoutActivityTypeCardioDance': 'workout_dance',

    # --- INNE ---
    'HKCategoryTypeIdentifierMenstrualFlow': 'menstr'
}


def write_tables_to_db(data_tables, db_path=DB_PATH):
    if not data_tables:
        print("Brak danych do zapisania do bazy.")
        return

    print(f" Rozpoczynam proces budowania bazy: {db_path}")
    conn = sqlite3.connect(db_path)

    for table_name, df in data_tables.items():
        t_name = table_name.lower()
        print(f"\n Przetwarzanie: {t_name}...")

        df.to_sql(f"raw_{t_name}", conn, if_exists='replace', index=False)
        print(f" Zapisano wersję RAW ({len(df)} rekordów)")

        # --- WERSJA CZYSTA (CLEAN) ---
        df_cleaned = clean_data(df, t_name)
        df_cleaned.to_sql(f"clean_{t_name}", conn, if_exists='replace', index=False)
        print(f"  ✨ Zapisano wersję CLEAN ({len(df_cleaned)} rekordów)")

    # 2. DODAWANIE INDEKSÓW (Tylko dla tabel CLEAN, bo na nich będzie pracować apka)
    print("\n⚡ Optymalizacja bazy (indeksy)...")
    cursor = conn.cursor()

    # Automatyczne tworzenie indeksów na datach dla wszystkich tabel 'clean_'
    for table_name in data_tables.keys():
        t_name = table_name.lower()
        try:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{t_name}_date ON clean_{t_name}(startDate)")
        except:
            # Niektóre tabele (np. Profile) mogą nie mieć startDate
            pass

    conn.commit()
    conn.close()
    print("\nBaza danych gotowa.\n")


def setup_database():
    # 1. Wczytujemy dane (Tutaj używamy Twojej funkcji parsera)
    data_tables = load_all_health_data(XML_PATH, short_names)
    write_tables_to_db(data_tables, DB_PATH)



def delete_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
