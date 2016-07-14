from __future__ import unicode_literals
from ..baseapi import BaseApi
from ..helpers import merge_two_dicts 


class Member(BaseApi):

    def __init__(self, *args, **kwargs):
        super(Member, self).__init__(*args, **kwargs)
        self.endpoint = 'lists'

    def all(self, list_id, get_all=False, **kwargs):
        """
        returns the first 10 members for a specific list
        or if get_all=True return all
        """
        # Get total amount of members in the list
        total = self._mc_client._get(url=self._build_path(list_id, 'members'), **kwargs)['total_items']
        # Itterate by 100 if more
        if get_all and total > 100:
            ret = {}
            for offset in range(0, int(total /100) +1):
                ret = merge_two_dicts(ret, self._mc_client._get(url=self._build_path(list_id, 'members'), 
                        offset=int(offset*100), count=100, **kwargs))
            return ret
        elif get_all and total <= 100:
            return self._mc_client._get(url=self._build_path(list_id, 'members'), count=total, **kwargs)
        else:
            return self._mc_client._get(url=self._build_path(list_id, 'members'), **kwargs)

    def get(self, list_id, member_id):
        """
        returns the specified list member.
        """
        return self._mc_client._get(url=self._build_path(list_id, 'members', member_id))

    def update(self, list_id, member_id, data):
        """
        updates an existing list member.
        """
        return self._mc_client._patch(url=self._build_path(list_id, 'members', member_id), data=data)

    def delete(self, list_id, member_id):
        """
        removes an existing list member from the list. This cannot be undone.
        """
        return self._mc_client._delete(url=self._build_path(list_id, 'members', member_id))

    def create(self, list_id, data):
        """
        adds a new member to the list.
        """
        return self._mc_client._post(url=self._build_path(list_id, 'members'), data=data)

    def create_or_update(self, list_id, member_id, data):
        """
        adds or updates an existing list member.
        """
        return self._mc_client._put(url=self._build_path(list_id, 'members', member_id), data=data)
