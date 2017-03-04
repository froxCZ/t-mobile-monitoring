/**
 * Created by vojtech.udrzal on 3/4/17.
 */
import Moment from "moment";
export default class Util {
  static formatIsoDateString(isoDateString, format) {
    return Moment(isoDateString, "YYYY-MM-DDThh:mm:ssTZD").format(format)
  }
}