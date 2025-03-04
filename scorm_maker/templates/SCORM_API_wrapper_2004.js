/*
SCORM API Wrapper for SCORM 2004
*/

class SCORM_API {
    constructor() {
        this.api = null;
        this.findAPI(window);
    }
    
    findAPI(win) {
        let findAPITries = 0;
        while ((win.API_1484_11 == null) && (win.parent != null) && (win.parent != win)) {
            findAPITries++;
            if (findAPITries > 7) {
                console.error("Error finding API -- too deeply nested.");
                return null;
            }
            win = win.parent;
        }
        this.api = win.API_1484_11;
    }
    
    initialize() {
        if (this.api == null) {
            console.error("SCORM API not found.");
            return false;
        }
        
        const result = this.api.Initialize("");
        console.log("Initialize result:", result);
        
        if (result === "true" || result === true) {
            // Set initial values
            this.setValue("cmi.completion_status", "incomplete");
            this.setValue("cmi.success_status", "unknown");
            this.setValue("cmi.score.min", "0");
            this.setValue("cmi.score.max", "100");
            return true;
        }
        
        return false;
    }
    
    terminate() {
        if (this.api == null) {
            return false;
        }
        
        const result = this.api.Terminate("");
        console.log("Terminate result:", result);
        
        return (result === "true" || result === true);
    }
    
    getValue(element) {
        if (this.api == null) {
            return "";
        }
        
        const value = this.api.GetValue(element);
        const error = this.api.GetLastError();
        
        if (error !== "0") {
            console.error(`GetValue('${element}') failed. Error code: ${error}`);
            return "";
        }
        
        return value;
    }
    
    setValue(element, value) {
        if (this.api == null) {
            return false;
        }
        
        const result = this.api.SetValue(element, value);
        const error = this.api.GetLastError();
        
        if (error !== "0") {
            console.error(`SetValue('${element}', '${value}') failed. Error code: ${error}`);
            return false;
        }
        
        return (result === "true" || result === true);
    }
    
    commit() {
        if (this.api == null) {
            return false;
        }
        
        const result = this.api.Commit("");
        const error = this.api.GetLastError();
        
        if (error !== "0") {
            console.error(`Commit failed. Error code: ${error}`);
            return false;
        }
        
        return (result === "true" || result === true);
    }
}
