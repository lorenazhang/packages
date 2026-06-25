SELECT

    DatabaseName,

    TableName,

    ColumnName

FROM DBC.ColumnsV

WHERE DatabaseName = 'YOUR_SCHEMA'

  AND UPPER(ColumnName) = 'OPR_APPLICATION_NR'

  AND TableName LIKE 'DLY_CR_%'

ORDER BY TableName;
