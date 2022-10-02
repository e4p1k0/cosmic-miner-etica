var LocalStorage = require('node-localstorage').LocalStorage;
const fs = require('fs');
const path = require('path');
var logStorage;
var errorLog = [];
var stdLog = [];

module.exports = {
    init(vault) {
        this.vault = vault;
        //logStorage = new LocalStorage(vault.get0xBitcoinLocalFolderPath() + '/logs');
        logStorage = new LocalStorage(vault.get0xBitcoinLocalFolderPath() + '/logs', 64 * 1024 * 1024);

        if (this.logsExist()) {
            errorLog = JSON.parse(logStorage.getItem('error'));
            stdLog = JSON.parse(logStorage.getItem('stdout'));
        }

        // FIXME/TODO: logging temporarily disabled in +HB v3.4t due to Quota exceeded errors reported by users.
        //              currently investigating this.
        //this.saveLogs();
    },

    logsExist() {
        if (!fs.existsSync(this.vault.get0xBitcoinLocalFolderPath()) || !fs.existsSync(this.vault.get0xBitcoinLocalFolderPath() + '/logs')) {
            return false;
        }

        if (!fs.existsSync(this.vault.get0xBitcoinLocalFolderPath() + '/logs/stdout')) {
            return false;
        }

        return true;
    },

    appendToStandardLog(s) {
        if (stdLog.length > 1000) {
            stdLog = []
        }

        var newline = ""
        newline += this.getDateTime()
        newline += s
        newline += '\\n';

        stdLog.push(newline)
        this.saveLogs();
    },

    appendToErrorLog(s) {
        if (errorLog.length > 1000) {
            errorLog = []
        }

        var newline = ""
        newline += this.getDateTime()
        newline += s
        newline += '\\n';

        errorLog.push(newline)
        this.saveLogs();
    },

    saveLogs() {
        try {
            logStorage.setItem('stdout', JSON.stringify(stdLog));
            logStorage.setItem('error', JSON.stringify(errorLog));
        } catch (e) {
            console.log('logging save error ', e)
        }
    },

    getDateTime() {
        var date = new Date();
        var hour = date.getHours();
        hour = (hour < 10 ? "0" : "") + hour;

        var min = date.getMinutes();
        min = (min < 10 ? "0" : "") + min;

        var sec = date.getSeconds();
        sec = (sec < 10 ? "0" : "") + sec;

        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        month = (month < 10 ? "0" : "") + month;

        var day = date.getDate();
        day = (day < 10 ? "0" : "") + day;

        return year + ":" + month + ":" + day + ":" + hour + ":" + min + ":" + sec;
    },

    print() {
        var date = new Date();
        var stamp = "\x1b[?25l\x1b[2K\x1b[1G\x1b[38;5;249m[" + 
                    date.getHours().toString().padStart(2, "0") + ":" +
                    date.getMinutes().toString().padStart(2, "0") + ":" +
                    date.getSeconds().toString().padStart(2, "0") + "." +
                    date.getMilliseconds().toString().padStart(3, "0") +
                    "]\x1b[0m";
        console.log(stamp, ...arguments);
        return process.stdout.write('\x1b[?25h');
    }
}
