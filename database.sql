-- Table for storing countries
CREATE TABLE Country (
    CountryID INTEGER PRIMARY KEY,
    CountryName TEXT NOT NULL,
    Region TEXT,
    Population INTEGER,
    VaccineType TEXT
);

-- Table for storing US states and their associated data
CREATE TABLE USState (
    StateID INTEGER PRIMARY KEY,
    StateName TEXT NOT NULL,
    CountryID INTEGER,
    DosesGiven INTEGER,
    FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
);

-- Table for storing age group data
CREATE TABLE AgeGroup (
    AgeGroupID INTEGER PRIMARY KEY,
    AgeRange TEXT NOT NULL,
    DosesGiven INTEGER,
    CountryID INTEGER,
    FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
);

-- Table for storing vaccine data
CREATE TABLE Vaccine (
    VaccineID INTEGER PRIMARY KEY,
    VaccineName TEXT NOT NULL,
    Manufacturer TEXT
);

-- Table for associating vaccines with manufacturers and countries
CREATE TABLE VaccineManufacturer (
    ManufacturerID INTEGER PRIMARY KEY,
    VaccineID INTEGER,
    CountryID INTEGER,
    Date DATE,
    DosesGiven INTEGER,
    FOREIGN KEY (VaccineID) REFERENCES Vaccine(VaccineID),
    FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
);

-- Table for daily vaccination data
CREATE TABLE DaileyVaccinationData (
    CountryID INTEGER,
    Date DATE NOT NULL,
    DosesGiven INTEGER,
    PeopleVaccinated INTEGER,
    PeopleFullyVaccinated INTEGER,
    BoostersGiven INTEGER,
    PRIMARY KEY (CountryID, Date),
    FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
);

-- Table for storing vaccination data in general
CREATE TABLE Vaccination (
    VaccinationID INTEGER PRIMARY KEY,
    CountryID INTEGER,
    VaccineID INTEGER,
    Date DATE,
    DosesGiven INTEGER,
    PeopleVaccinated INTEGER,
    PeopleFullyVaccinated INTEGER,
    TotalBoostersGiven INTEGER,
    FOREIGN KEY (CountryID) REFERENCES Country(CountryID),
    FOREIGN KEY (VaccineID) REFERENCES Vaccine(VaccineID)
);