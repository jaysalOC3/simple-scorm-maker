/*
SCORM API Wrapper for SCORM 1.2
*/

class SCORM_API {
    constructor() {
        this.api = null;
        this.findAPI(window);
    }
    
    findAPI(win) {
        let findAPITries = 0;
        while ((win.API == null) && (win.parent != null) && (win.parent != win)) {
            findAPITries++;
            if (findAPITries > 7) {
                console.error("Error finding API -- too deeply nested.");
                return null;
            }
            win = win.parent;
        }
        this.api = win.API;
    }
    
    initialize() {
        if (this.api == null) {
            console.error("SCORM API not found.");
            return false;
        }
        
        const result = this.api.LMSInitialize("");
        console.log("LMSInitialize result:", result);
        
        if (result === "true" || result === true) {
            // Set initial values
            this.setValue("cmi.core.lesson_status", "incomplete");
            this.setValue("cmi.core.score.min", "0");
            this.setValue("cmi.core.score.max", "100");
            return true;
        }
        
        return false;
    }
    
    terminate() {
        if (this.api == null) {
            return false;
        }
        
        const result = this.api.LMSFinish("");
        console.log("LMSFinish result:", result);
        
        return (result === "true" || result === true);
    }
    
    getValue(element) {
        if (this.api == null) {
            return "";
        }
        
        const value = this.api.LMSGetValue(element);
        const error = this.api.LMSGetLastError();
        
        if (error !== "0") {
            console.error(`LMSGetValue('${element}') failed. Error code: ${error}`);
            return "";
        }
        
        return value;
    }
    
    setValue(element, value) {
        if (this.api == null) {
            return false;
        }
        
        const result = this.api.LMSSetValue(element, value);
        const error = this.api.LMSGetLastError();
        
        if (error !== "0") {
            console.error(`LMSSetValue('${element}', '${value}') failed. Error code: ${error}`);
            return false;
        }
        
        return (result === "true" || result === true);
    }
    
    commit() {
        if (this.api == null) {
            return false;
        }
        
        const result = this.api.LMSCommit("");
        const error = this.api.LMSGetLastError();
        
        if (error !== "0") {
            console.error(`LMSCommit failed. Error code: ${error}`);
            return false;
        }
        
        return (result === "true" || result === true);
    }
}
