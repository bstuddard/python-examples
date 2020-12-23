let
    // Read in input csv
    Source = Csv.Document(
        File.Contents("D:\test_data.csv"),
        [
            Delimiter=",", 
            Columns=3, 
            Encoding=1252, 
            QuoteStyle=QuoteStyle.None
        ]
    ),

    // Promote headers and update types
    headers_promoted = Table.PromoteHeaders(
        Source, 
        [PromoteAllScalars=true]
    ),
    type_changes = Table.TransformColumnTypes(
        headers_promoted,
        {
            {"square_footage", Int64.Type}, 
            {"number_of_rooms", Int64.Type}, 
            {"price", Int64.Type}
        }
    ),

    // Build API Parms
    api_url = "https://username.pythonanywhere.com/HousingClustering",
    content_input = Json.FromValue(type_changes),
    header = [
        #"Content-Type"="application/json", 
        #"accept"="application/json"
    ],

    // Make API call
    web_results = Json.Document(
        Web.Contents(
            api_url, 
            [Content=content_input]
        )
    ),

    // Convert api results to a table
    json_doc = Json.Document(web_results),
    table_from_list = Table.FromRecords(json_doc),
    update_types = Table.TransformColumnTypes(
        table_from_list, 
        {
            {"row", Int64.Type}, 
            {"group", Int64.Type}
        }
    ),

    // Join source and results
    idx = Table.AddIndexColumn(
        type_changes, 
        "Index",  // Col Name
        1,        // Initial
        1,        // Increment
        Int64.Type
    ),
    joined_tables = Table.Join(
        idx,      // Table 1
        "Index",  // Join Col 1
        update_types, // Table 2
        "row"         // Join Col 2
    ),
    final_cols = Table.RemoveColumns(
        joined_tables, 
        {"Index", "row"}
    )
in
    final_cols