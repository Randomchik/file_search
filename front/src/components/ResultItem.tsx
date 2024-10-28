import { Spin, Alert } from "antd"
import { SearchRequest } from "../features/searchSlice"

interface ResultItemProps {
  record: SearchRequest
  loadingResults: Record<string, boolean>
  results: Record<string, string[]>
}

export function ResultItem({
  record,
  loadingResults,
  results,
}: ResultItemProps) {
  return (
    <>
      {loadingResults[record.id] ? (
        <Spin tip="Loading results..." />
      ) : record.finished && results[record.id] ? (
        results[record.id].length > 0 ? (
          <ul>
            {results[record.id].map((result, index) => (
              <li key={index}>{result}</li>
            ))}
          </ul>
        ) : (
          <Alert message="No results found" type="warning" showIcon />
        )
      ) : (
        <Alert message="Search is still in progress" type="info" showIcon />
      )}
    </>
  )
}
