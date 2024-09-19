query_creacion_bbdd = "CREATE SCHEMA IF NOT EXISTS `Proyecto` DEFAULT CHARACTER SET utf8mb4;"

query_creacion_tabla_employees = """
                            CREATE TABLE IF NOT EXISTS `employees` (
                            `idemployee` INT NOT NULL AUTO_INCREMENT,
                            `EmployeeNumber` VARCHAR(45) NULL,
                            `Age` INT UNSIGNED NULL,
                            `Gender` VARCHAR(45) NULL,
                            `Education` INT UNSIGNED NULL,
                            `EducationField` VARCHAR(45) NULL,
                            `NumCompaniesWorked` INT UNSIGNED NULL,
                            `MonthlyIncome` INT UNSIGNED NULL,
                            `StockOptionLevel` INT NULL,
                            `YearsAtCompany` INT UNSIGNED NULL,
                            `YearsSinceLastPromotion` INT UNSIGNED NULL,
                            `YearsWithCurrManager` INT UNSIGNED NULL,
                            `TrainingTimesLastYear` INT UNSIGNED NULL,
                            `DistanceFromHome` INT UNSIGNED NULL,
                            `Attrition` VARCHAR(45) NOT NULL,
                            `idwork` INT NOT NULL,
                            `idSatisfaction` INT NOT NULL,
                            PRIMARY KEY (`idemployee`),
                            INDEX `fk_employees_work_idx` (`idwork` ASC) VISIBLE,
                            INDEX `fk_employees_Satisfaction_Surveys1_idx` (`idSatisfaction` ASC) VISIBLE,
                            CONSTRAINT `fk_employees_work`
                                FOREIGN KEY (`idwork`)
                                REFERENCES `proyecto`.`work` (`idwork`)
                                ON DELETE CASCADE
                                ON UPDATE CASCADE,
                            CONSTRAINT `fk_employees_Satisfaction_Surveys1`
                                FOREIGN KEY (`idSatisfaction`)
                                REFERENCES `proyecto`.`Satisfaction_Surveys` (`idSatisfaction`)
                                ON DELETE CASCADE
                                ON UPDATE CASCADE)
                            ENGINE = InnoDB;
                            """
                            
query_creacion_tabla_work = """
                            CREATE TABLE IF NOT EXISTS `work` (
                            `idWork` INT NOT NULL AUTO_INCREMENT,
                            `JobLevel` INT UNSIGNED NOT NULL,
                            `JobRole` VARCHAR(45) NOT NULL,
                            `Department` VARCHAR(45) NULL,
                            PRIMARY KEY (`idWork`))
                            ENGINE = InnoDB;
                            """


query_creacion_tabla_work_info = """
                                CREATE TABLE IF NOT EXISTS `work_info` (
                                `idwork_info` INT NOT NULL AUTO_INCREMENT,
                                `RemoteWork` VARCHAR(45) NOT NULL,
                                `OverTime` VARCHAR(45) NULL,
                                `BusinessTravel` VARCHAR(45) NULL,
                                `idwork` INT NOT NULL,
                                PRIMARY KEY (`idwork_info`),
                                INDEX `fk_work_info_work1_idx` (`idwork` ASC) VISIBLE,
                                CONSTRAINT `fk_work_info_work1`
                                    FOREIGN KEY (`idwork`)
                                    REFERENCES `proyecto`.`work` (`idwork`)
                                    ON DELETE CASCADE
                                    ON UPDATE CASCADE)
                                ENGINE = InnoDB;
                                    """


query_creacion_tabla_satisfaction_surveys = """
                                    CREATE TABLE IF NOT EXISTS `satisfaction_surveys` (
                                    `idSatisfaction` INT NOT NULL AUTO_INCREMENT,
                                    `JobInvolvement` INT UNSIGNED NULL,
                                    `PerformanceRating` INT UNSIGNED NULL,
                                    `EnvironmentSatisfaction` INT UNSIGNED NULL,
                                    `RelationshipSatisfaction` INT UNSIGNED NULL,
                                    `WorkLifeBalance` INT UNSIGNED NULL,
                                    `JobSatisfaction` INT UNSIGNED NULL,
                                    PRIMARY KEY (`idSatisfaction`))
                                    ENGINE = InnoDB;"""
                                    
query_insercion_employees = """INSERT INTO employees (
                                    EmployeeNumber, 
                                    Age, 
                                    Gender, 
                                    Education, 
                                    EducationField, 
                                    NumCompaniesWorked, 
                                    MonthlyIncome, 
                                    StockOptionLevel,
                                    YearsAtCompany, 
                                    YearsSinceLastPromotion,
                                    YearsWithCurrManager,
                                    TrainingTimesLastYear,                               
                                    DistanceFromHome, 
                                    Attrition,
                                    idWork,
                                    idSatisfaction) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

   

query_insercion_work = "INSERT INTO work (JobLevel, JobRole, Department) VALUES (%s, %s, %s)"
query_insercion_satisfaction = """INSERT INTO satisfaction_surveys (
                                    JobInvolvement, 
                                    PerformanceRating, 
                                    EnvironmentSatisfaction, 
                                    RelationshipSatisfaction, 
                                    WorkLifeBalance, 
                                    JobSatisfaction) 
                                    VALUES (%s, %s, %s, %s, %s, %s)"""

query_insercion_work_info = """INSERT INTO work_info (
                                RemoteWork,
                                OverTime,
                                BusinessTravel,
                                idWork)
                                VALUES (%s, %s, %s, %s)"""