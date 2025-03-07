// Library
import { ref } from 'vue';
import Cookies from 'js-cookie';
import localForage from 'localforage';

// Types
import type { Ref } from 'vue';
type StorageMode = 'memory' | 'disk' | 'diskOnly';

// Global cache object
const cache: Ref<Record<string, object>> = ref({});


/**
 * Save a particular key and value to in memory cache.
 * @param key Key to save the in memory cache item to.
 * @param value Value to save the in memory cache item to.
 */
function setMemoryCache(key: string, value: any): void {
    cache.value[key] = value;
}


/**
 * Save a particular key and value to disk cache.
 * @param key Key to save disk cache to.
 * @param value Object to save disk cache to.
 */
function setDiskCache(key: string, value: any): void {
    localStorage.setItem(key, JSON.stringify(value));
}


/**
 * Get a cached object from memory.
 * @param key Key to use to get memory cache object.
 * @returns Cached object.
 */
function getMemoryCache(key: string): any {
    const cachedValue: any = cache.value[key];
    if (cachedValue === null){
        return null;
    }
    return cachedValue;
}


/**
 * Get a cached object from disk.
 * @param key Key to use to get the disk cache.
 * @returns Cached object.
 */
function getDiskCache(key: string): any | null {
    const cachedValue: string | null = localStorage.getItem(key);
    if (cachedValue === null){
        return null;
    }

    try {
        return JSON.parse(cachedValue);
    } catch (error){
        return cachedValue;
    }
}


/**
 * Check if key exists in memory cache.
 * @param key Key to check if it exists in memory cache.
 * @returns true or false as to whether key exists in memory cache.
 */
function hasMemoryCache(key: string): boolean {
    return key in cache.value;
}


/**
 * Check if key exists in disk cache.
 * @param key Key to check if it exists in disk cache.
 * @returns true or false as to whether key exists in disk cache.
 */
function hasDiskCache(key: string): boolean {
    return localStorage.getItem(key) !== null;
}



/**
 * Save item to cache based on layer chosen.
 * @param key Key to use to set the cache.
 * @param value Object to save to cache.
 * @param storageMode memory, disk, or diskOnly. Defaults to memory. Cache layer to store as.
 */
function setCache(key: string, value: any, storageMode: StorageMode = 'memory'): void {
    if (storageMode === 'memory' || storageMode === 'disk'){
        setMemoryCache(key, value);
    }
    if (storageMode === 'disk' || storageMode === 'diskOnly'){
        setDiskCache(key, value);
    }
}


/**
 * Checks if key exists in memory cache then disk cache, returning the first available or null if nothing cached.
 * @param key Key to retrieve from cache.
 * @returns cached object.
 */
function getCache(key: string): any {
    if (hasMemoryCache(key)){
        return getMemoryCache(key);
    } else if (hasDiskCache(key)) {
        return getDiskCache(key);
    } else {
        return null;
    }
}


/**
 * Remove all items in local storage that start with a specific prefix.
 * @param prefix String prefix to use to search.
 * @param exclude Optional string. If a key contains this string, it won't be cleared.
 */
function clearAllDiskCacheWithPrefix(prefix: string, exclude?: string): void {
    for (let i = localStorage.length - 1; i >= 0; i--) {
        const key = localStorage.key(i);
        if (key && key.startsWith(prefix) && (!exclude || !key.includes(exclude))){
            localStorage.removeItem(key);
        }
    }
}


/**
 * Set cookie using js-cookie.
 */
function setCookie(key: string, value: string, days: number = 30): void {
    Cookies.set(key, value, { expires: days * 1, path: '/', secure: true, sameSite: 'Lax' });
}


/**
 * Get cookie using js-cookie.
 */
function getCookie(key: string): string | undefined {
    return Cookies.get(key);
}


/**
 * Clear a cookie using js-cookie.
 */
function clearCookie(key: string): void {
    Cookies.remove(key, { path: '/' });
}


/**
 * Save a particular key and value to IndexedDB cache.
 * @param key Key to save IndexedDB cache item to.
 * @param value Value to save to IndexedDB cache.
 */
async function setIndexedDBCache(key: string, value: any): Promise<void> {
    await localForage.setItem(key, value);
}

/**
 * Get a cached object from IndexedDB.
 * @param key Key to use to get IndexedDB cache object.
 * @returns Cached object or null.
 */
async function getIndexedDBCache(key: string): Promise<any | null> {
    return await localForage.getItem(key);
}


export default function useCache(){
    return {
        setCache,
        getCache,
        getDiskCache,
        clearAllDiskCacheWithPrefix,
        setCookie,
        getCookie,
        clearCookie,
        setIndexedDBCache,
        getIndexedDBCache
    }
}