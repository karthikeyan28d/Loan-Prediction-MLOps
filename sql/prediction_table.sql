CREATE TABLE Predictions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    Client_ID VARCHAR(255),  -- Stores the Client ID from frontend
    run_id VARCHAR(100),  -- MLflow Run ID
    prediction_date DATETIME DEFAULT GETDATE(),  -- Auto-fills with current timestamp
    input_data NVARCHAR(MAX),  -- Stores raw input JSON from frontend
    preprocessed_data NVARCHAR(MAX),  -- Stores preprocessed input before passing to the model
    prediction_probability FLOAT,  -- Probability score of default
    predicted_class INT  -- 1 = Default, 0 = No Default
);