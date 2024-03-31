import './ActivityItem.css';

import ActivityActionReply  from '../components/ActivityActionReply';
import ActivityActionRepost  from '../components/ActivityActionRepost';
import ActivityActionLike  from '../components/ActivityActionLike';
import ActivityActionShare  from '../components/ActivityActionShare';

import { Link } from "react-router-dom";
import { format_datetime, time_ago, time_future } from '../lib/DateTimeFormats';
import {ReactComponent as BombIcon} from './svg/bomb.svg';

export default function ActivityShowItem(props) {

  const attrs = {}
  attrs.class = 'activity_item expanded'
  return (
    <div {...attrs}>
      <div class="acitivty_main">
        <div class='activity_content_wrap'>
          <div class='activity_content'>
            <Link class='activity_avatar'to={`/@`+props.activity.handle} ></Link>
            <div class='activity_meta'>
              <div class='activity_identity' >
                <Link class='display_name' to={`/@`+props.activity.handle}>{props.activity.display_name}</Link>
                <Link class="handle" to={`/@`+props.activity.handle}>@{props.activity.handle}</Link>
              </div>{/* activity_identity */}
              <div class='activity_times'>
                <div class="created_at" title={format_datetime(props.activity.created_at)}>
                  <span class='ago'>{time_ago(props.activity.created_at)}</span> 
                </div>
                <div class="expires_at" title={format_datetime(props.activity.expires_at)}>
                  <BombIcon class='icon' />
                  <span class='ago'>{time_future(props.activity.expires_at)}</span>
                </div>
              </div>{/* activity_times */}
            </div>{/* activity_meta */}
          </div>{/* activity_content */}
          <div class="message">{props.activity.message}</div>
        </div>

        <div class='expandedMeta'>
          <div class="created_at">
            {format_datetime(props.activity.created_at)}
          </div>
        </div>
        <div class="activity_actions">
          <ActivityActionReply setReplyActivity={props.setReplyActivity} activity={props.activity} setPopped={props.setPopped} activity_uuid={props.activity.uuid} count={props.activity.replies_count}/>
          <ActivityActionRepost activity_uuid={props.activity.uuid} count={props.activity.reposts_count}/>
          <ActivityActionLike activity_uuid={props.activity.uuid} count={props.activity.likes_count}/>
          <ActivityActionShare activity_uuid={props.activity.uuid} />
        </div>
      </div>
    </div>
  )
}