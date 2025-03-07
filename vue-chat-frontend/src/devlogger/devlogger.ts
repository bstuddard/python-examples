type LogLevel = 'info' | 'warn' | 'error';
import useCache from "@/composables/useCache";
const { setCache } = useCache()

export function devlog(message: any, level: LogLevel = 'info', saveToStorage: boolean = false, storageSaveName: string | null = null): void {
    
    switch (level) {
        case 'error':
            console.error(message);
            break;
        case 'warn':
            console.warn(message);
            break;
        default:
            console.log(message);
            break;

    }

    // Save error message to storage if necessary. 
    if (saveToStorage && storageSaveName) {
        setCache(storageSaveName, message, 'disk');
    }
    
}


export function assert(condition: boolean, message?: string): void {
    if (!condition) {
        message = message || 'Assertion failed';
        throw new Error(message);
    }
}