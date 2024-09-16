query_creacion_bbdd = "CREATE SCHEMA IF NOT EXISTS `Proyecto` DEFAULT CHARACTER SET utf8mb4;"

query_creacion_tabla_employee = """
                            CREATE TABLE IF NOT EXISTS `employees` (
                            `idEmployee` INT NOT NULL AUTO_INCREMENT,
                            `EmployeeNumber` VARCHAR(45),
                            `Age` INT NULL,
                            `Education` INT NULL,
                            `NumCompaniesWorked` INT NULL,
                            `DistanceFromHome` INT UNSIGNED NULL,
                            PRIMARY KEY (`idEmployee`))
                            ENGINE = InnoDB;
                            """
                            
query_creacion_tabla_work = """
                            CREATE TABLE IF NOT EXISTS `work` (
                            `idWork` INT NOT NULL AUTO_INCREMENT,
                            `JobLevel` INT UNSIGNED NULL,
                            `JobRole` VARCHAR(45) NULL,
                            `Department` VARCHAR(45) NULL,
                            PRIMARY KEY (`idWork`))
                            ENGINE = InnoDB;
                            """

query_creacion_tabla_work_conditions = """
                                    CREATE TABLE IF NOT EXISTS `workconditions` (
                                    `idWork` INT NOT NULL,
                                    `RemoteWork` VARCHAR(45) NULL,
                                    `BusinessTravel` VARCHAR(45) NULL,
                                    `OverTime` VARCHAR(45) NULL,
                                    INDEX `fk_workconditions_work-type1_idx` (`idWork` ASC) VISIBLE,
                                    CONSTRAINT `fk_workconditions_work-type1`
                                        FOREIGN KEY (`idWork`)
                                        REFERENCES `mydb`.`work-type` (`idWork`)
                                        ON DELETE NO ACTION
                                        ON UPDATE NO ACTION)
                                    ENGINE = InnoDB;
                                    """

query_creacion_tabla_work_employee = """
                                    CREATE TABLE IF NOT EXISTS `employees_work` (
                                    `idEmployee` INT NOT NULL,
                                    `idWork` INT NOT NULL,
                                    PRIMARY KEY (`idEmployee`, `idWork`),
                                    INDEX `fk_employees_has_work-type_work-type1_idx` (`idWork` ASC) VISIBLE,
                                    INDEX `fk_employees_has_work-type_employees1_idx` (`idEmployee` ASC) VISIBLE,
                                    CONSTRAINT `fk_employees_has_work-type_employees1`
                                        FOREIGN KEY (`idEmployee`)
                                        REFERENCES `mydb`.`employees` (`idEmployee`)
                                        ON DELETE NO ACTION
                                        ON UPDATE NO ACTION,
                                    CONSTRAINT `fk_employees_has_work-type_work-type1`
                                        FOREIGN KEY (`idWork`)
                                        REFERENCES `mydb`.`work-type` (`idWork`)
                                        ON DELETE NO ACTION
                                        ON UPDATE NO ACTION)
                                    ENGINE = InnoDB;
                                    """

query_insercion_employees = "INSERT INTO employees (EmployeeNumber, Age, Education, NumCompaniesWorked, DistanceFromHome) VALUES (%s, %s, %s, %s, %s)"

query_insercion_work = "INSERT INTO work (JobLevel, JobRole, Department) VALUES (%s, %s, %s)"
