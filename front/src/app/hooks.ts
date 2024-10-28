import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';

import type { RootState, AppDispatch } from './store';

// Хук useAppDispatch с типом AppDispatch для типизации dispatch
export const useAppDispatch = () => useDispatch<AppDispatch>();

// Хук useAppSelector с типом RootState для типизации состояния
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
