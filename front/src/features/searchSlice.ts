import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit"
import { createSearch, getSearchResults } from "../api/searchApi"

export interface SearchRequest {
  id: string
  text?: string
  file_mask?: string
  size?: { value: number; operator: string }
  creation_time?: { value: string; operator: string }
  finished: boolean
}

interface SearchState {
  searches: SearchRequest[]
  results: { [key: string]: string[] } // Результаты поиска по `id`
  loadingResults: { [key: string]: boolean }
}

const initialState: SearchState = {
  searches: [],
  results: {},
  loadingResults: {},
}

// Создать новый поиск
export const createNewSearch = createAsyncThunk(
  "search/createNewSearch",
  async (data: Omit<SearchRequest, "id" | "finished" | "results">) => {
    const response = await createSearch(data)
    return { search_id: response.search_id, ...data }
  }
)

// Получить результаты поиска
export const fetchSearchResults = createAsyncThunk(
  "search/fetchSearchResults",
  async (searchId: string) => {
    return { searchId, ...(await getSearchResults(searchId)) }
  }
)

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(
        createNewSearch.fulfilled,
        (
          state,
          action
        ) => {
          const { search_id, text, file_mask, size, creation_time } =
            action.payload
          state.searches.push({
            id: search_id,
            text,
            file_mask,
            size,
            creation_time,
            finished: false,
          })
        }
      )
      .addCase(fetchSearchResults.pending, (state, action) => {
        state.loadingResults[action.meta.arg] = true
      })
      .addCase(
        fetchSearchResults.fulfilled,
        (
          state,
          action: PayloadAction<{
            searchId: string
            finished: boolean
            results: string[]
          }>
        ) => {
          const { searchId, finished, results: paths } = action.payload
          state.results[searchId] = paths
          const search = state.searches.find((s) => s.id === searchId)
          if (search) {
            search.finished = finished
          }
          state.loadingResults[searchId] = false
        }
      )
  },
})

export default searchSlice.reducer
