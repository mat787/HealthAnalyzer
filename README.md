📂 Analiza struktury danych (Research)
1. Plik export.xml

Główny plik bazy danych Apple Health. Zastosowano podejście iteracyjne (iterparse), aby zoptymalizować zużycie pamięci RAM przy przetwarzaniu dużych zbiorów (400k+ rekordów).

Pomijamy Correlation, 

Podstawowe informacje o użytkowniku:
*     HKCharacteristicTypeIdentifierDateOfBirth                   
*     HKCharacteristicTypeIdentifierBiologicalSex                 CDATA #REQUIRED
*     HKCharacteristicTypeIdentifierBloodType                     CDATA #REQUIRED
*     HKCharacteristicTypeIdentifierFitzpatrickSkinType           CDATA #REQUIRED
*     HKCharacteristicTypeIdentifierCardioFitnessMedicationsUse   CDATA #REQUIRED

<!ELEMENT Record ((MetadataEntry|HeartRateVariabilityMetadataList)*)>
<!ATTLIST Record
  type          CDATA #REQUIRED
  unit          CDATA #IMPLIED
  value         CDATA #IMPLIED
  sourceName    CDATA #REQUIRED
  sourceVersion CDATA #IMPLIED
  device        CDATA #IMPLIED
  creationDate  CDATA #IMPLIED
  startDate     CDATA #REQUIRED
  endDate       CDATA #REQUIRED
>

<!ELEMENT Workout ((MetadataEntry|WorkoutEvent|WorkoutRoute|WorkoutStatistics)*)>
<!ATTLIST Workout
  workoutActivityType   CDATA #REQUIRED
  duration              CDATA #IMPLIED
  durationUnit          CDATA #IMPLIED
  totalDistance         CDATA #IMPLIED
  totalDistanceUnit     CDATA #IMPLIED
  totalEnergyBurned     CDATA #IMPLIED
  totalEnergyBurnedUnit CDATA #IMPLIED
  sourceName            CDATA #REQUIRED
  sourceVersion         CDATA #IMPLIED
  device                CDATA #IMPLIED
  creationDate          CDATA #IMPLIED
  startDate             CDATA #REQUIRED
  endDate               CDATA #REQUIRED
>
<!ELEMENT WorkoutActivity ((MetadataEntry)*)>
<!ATTLIST WorkoutActivity
  uuid                 CDATA #REQUIRED
  startDate            CDATA #REQUIRED
  endDate              CDATA #IMPLIED
  duration             CDATA #IMPLIED
  durationUnit         CDATA #IMPLIED
>
<!ELEMENT WorkoutEvent ((MetadataEntry)*)>
<!ATTLIST WorkoutEvent
  type                 CDATA #REQUIRED
  date                 CDATA #REQUIRED
  duration             CDATA #IMPLIED
  durationUnit         CDATA #IMPLIED
>
<!ELEMENT WorkoutStatistics EMPTY>
<!ATTLIST WorkoutStatistics
  type                 CDATA #REQUIRED
  startDate            CDATA #REQUIRED
  endDate              CDATA #REQUIRED
  average              CDATA #IMPLIED
  minimum              CDATA #IMPLIED
  maximum              CDATA #IMPLIED
  sum                  CDATA #IMPLIED
  unit                 CDATA #IMPLIED
>
<!ELEMENT WorkoutRoute ((MetadataEntry|FileReference)*)>
<!ATTLIST WorkoutRoute
  sourceName    CDATA #REQUIRED
  sourceVersion CDATA #IMPLIED
  device        CDATA #IMPLIED
  creationDate  CDATA #IMPLIED
  startDate     CDATA #REQUIRED
  endDate       CDATA #REQUIRED
>
<!ELEMENT FileReference EMPTY>
<!ATTLIST FileReference
  path CDATA #REQUIRED
>
<!ELEMENT ActivitySummary EMPTY>
<!ATTLIST ActivitySummary
  dateComponents           CDATA #IMPLIED
  activeEnergyBurned       CDATA #IMPLIED
  activeEnergyBurnedGoal   CDATA #IMPLIED
  activeEnergyBurnedUnit   CDATA #IMPLIED
  appleMoveTime            CDATA #IMPLIED
  appleMoveTimeGoal        CDATA #IMPLIED
  appleExerciseTime        CDATA #IMPLIED
  appleExerciseTimeGoal    CDATA #IMPLIED
  appleStandHours          CDATA #IMPLIED
  appleStandHoursGoal      CDATA #IMPLIED
>
<!ELEMENT MetadataEntry EMPTY>
<!ATTLIST MetadataEntry
  key   CDATA #REQUIRED
  value CDATA #REQUIRED
>
<!-- Note: Heart Rate Variability records captured by Apple Watch may include an associated list of instantaneous beats-per-minute readings. -->
<!ELEMENT HeartRateVariabilityMetadataList (InstantaneousBeatsPerMinute*)>
<!ELEMENT InstantaneousBeatsPerMinute EMPTY>
<!ATTLIST InstantaneousBeatsPerMinute
  bpm  CDATA #REQUIRED
  time CDATA #REQUIRED
>





2. Dane EKG (CSV)

Dane surowe pobierane z folderu electrocardiograms/.

    Częstotliwość próbkowania: 512 Hz.

    Odprowadzenie: I (Lead I).

    Jednostki: Napięcie wyrażone w mikrowoltach (μV), przeliczane na miliwolty (mV) na potrzeby analizy.