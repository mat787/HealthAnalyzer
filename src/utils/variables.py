
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