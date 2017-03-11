/**
 * Created by vojtech.udrzal on 3/4/17.
 */
import Moment from "moment";
Moment.locale('cs')

export default class Util {
  static formatIsoDateString(isoDateString, format) {
    return Moment(isoDateString, "YYYY-MM-DDThh:mm:ssTZD").format(format)
  }

  static parseIsoDateString(isoDateString) {
    return Moment(isoDateString, "YYYY-MM-DDThh:mm:ssTZD")
  }

}