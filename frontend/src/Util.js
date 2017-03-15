/**
 * Created by vojtech.udrzal on 3/4/17.
 */
import Moment from "moment";
Moment.locale('cs')


export default class Util {
  static formatIsoDateString(isoDateString, format) {
    return Moment(isoDateString, "YYYY-MM-DDThh:mm:ssTZD").format(format)
  }

  static formatIsoDateStrToDateTimeStr(isoDateString) {
    let m = Moment(isoDateString, "YYYY-MM-DDThh:mm:ssTZD")
    return m.format("L") + " " + m.format("LTS")
  }

  static parseIsoDateString(isoDateString) {
    return Moment(isoDateString, "YYYY-MM-DDThh:mm:ssTZD")
  }

  static timeAgo(momentTime) {
    let seconds = Math.floor(Moment.duration(Util.getCurrentTime().diff(momentTime)).asMilliseconds() / 1000)
    if (seconds < 60) {
      return seconds+ "s ago"
    }else if(seconds<60*60){
      let minutes = Math.floor(seconds/(60));
      let sec = Math.floor(seconds-minutes*60);
      return minutes+"m "+sec+"s ago";
    }else{
      let hours = Math.floor(seconds/(60*60))
      let minutes = Math.floor((seconds-hours*60*60)/60)
      return hours+"h "+minutes+"m ago";
    }

  }

  static getCurrentTime() {
    return Moment().subtract(Util.serverTimeDiff)
  }

  static setServerTimeDifference(serverTimeDiff) {
    Util.serverTimeDiff = serverTimeDiff
  }

  static isValidJson(str) {
    try {
      JSON.parse(str);
    } catch (e) {
      return false;
    }
    return true;
  }

  static countryToFlagPath(country) {
    let COUNTRY_TO_FLAG = {
      "CZ": "/img/flags/Czech Republic.png",
      "AT": "/img/flags/Austria.png",
      "NL": "/img/flags/Netherlands.png",
      "DE": "/img/flags/Germany.png",
    }
    return COUNTRY_TO_FLAG[country]
  }

}