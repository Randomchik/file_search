import React, { useCallback } from "react"
import { Table, Button } from "antd"

import { useAppSelector, useAppDispatch } from "../app/hooks"
import { fetchSearchResults } from "../features/searchSlice"
import type { SearchRequest } from "../features/searchSlice"

import { ResultItem } from "./ResultItem"

const SearchList: React.FC = () => {
  const searches = useAppSelector((state) => state.search.searches)
  const results = useAppSelector((state) => state.search.results)
  const loadingResults = useAppSelector((state) => state.search.loadingResults)
  const dispatch = useAppDispatch()

  const fetchResults = useCallback(
    (id: string) => {
      if (!results[id]) {
        dispatch(fetchSearchResults(id))
      }
    },
    [results]
  )

  const columns = [
    { title: "ID", dataIndex: "id", key: "id" },
    {
      title: "Filters",
      dataIndex: "filters",
      key: "filters",
      render: (_: any, record: SearchRequest) => {
        const { text, file_mask, size, creation_time } = record
        const filters = {
          text,
          file_mask,
          size,
          creation_time,
        }
        return (
          <pre>{JSON.stringify(filters, null).replace(/[\[\]\{\}]+/g, "")}</pre>
        )
      },
    },
    {
      title: "Status",
      dataIndex: "finished",
      key: "finished",
      render: (finished: boolean) => (finished ? "Finished" : "In Progress"),
    },
    {
      title: "Actions",
      key: "actions",
      render: () => (
        <Button >Show Results</Button>
      ),
    },
  ]

  return (
    <>
      <Table
        dataSource={searches}
        columns={columns}
        rowKey="id"
        pagination={{ pageSize: 5 }}
        expandable={{
          expandRowByClick: true,
          onExpand: (_: any, record: SearchRequest) => fetchResults(record.id),
          expandedRowRender: (record: SearchRequest) => (
            <ResultItem
              record={record}
              results={results}
              loadingResults={loadingResults}
            />
          ),
        }}
      />
    </>
  )
}

export default SearchList
