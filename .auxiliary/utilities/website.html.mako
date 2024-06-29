<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Available Releases</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
    </style>
</head>
<body>
    <h1>Available Releases</h1>
    <table>
        <thead>
            <tr>
                <th>Version</th>
                <th>Documentation</th>
                <th>Coverage</th>
            </tr>
        </thead>
        <tbody>
        % for version, attributes in versions.items():
            <tr>
                <td>${version}</td>
                <td>
                % if 'sphinx-html' in attributes:
                    <a href="${version}/sphinx-html/index.html">Docs</a>
                % else:
                    N/A
                % endif
                </td>
                <td>
                % if 'coverage-pytest' in attributes:
                    <a href="${version}/coverage-pytest/index.html">Coverage</a>
                % else:
                    N/A
                % endif
                </td>
            </tr>
        % endfor
        </tbody>
    </table>
</body>
</html>
