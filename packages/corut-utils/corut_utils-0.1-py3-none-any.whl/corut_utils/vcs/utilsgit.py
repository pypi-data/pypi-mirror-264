#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
We wanted to make it easier to read and manipulate
Git Repo data using the GitPython package.
The purpose here is to read the files and folders in the repo and detail
them and make sense of them.
"""

__all__ = (
    'GetRepo',
)

from typing import Union, Dict, List

from git import Repo
from git.types import Commit_ish
from pandas import DataFrame


class GetRepo(Repo):
    def __get_details(self, entry, revision) -> Dict:
        detail = [i for i in self.iter_commits(rev=revision, paths=entry.path)]
        return {
            'name': entry.name,
            'path': entry.path,
            'size': entry.size,
            'type': entry.type,
            'type2': 0 if entry.type == 'tree' else 1,
            'message': detail[0].message,
            'commit_time': detail[0].committed_datetime,
        }
    
    def get_commit_count(
            self, revision: Union[str, Commit_ish, None] = None
    ) -> int:
        """
        The total number of commits is returned as an integer.
        :param revision:
        :return: int value
        """
        return self.commit(rev=revision).count()
    
    def get_tag_count(self) -> int:
        """
        The total number of tags is returned as an integer.
        :return: int value
        """
        return self.tags.__len__()
    
    def get_branch_list(self) -> List[str]:
        """
        First it takes the branch list and sorts it. If there is a value such
        as 'main' or 'master' in the list, it puts it at the top of the list.
        
        :return: Returns the branch list.
        """
        branches = list(map(str, self.heads))
        branches.sort()
        for branch in ('main', 'master'):
            if branch in branches:
                branches.remove(branch)
                branches.insert(0, branch)
        return branches
    
    def get_files(
            self,
            revision: Union[str, Commit_ish, None] = None,
            path: str = None
    ) -> Dict | List[Dict]:
        """
        Gets and sorts all the details of the files in the specified
        directory for any revision.
        
        :param revision: If revision is left blank, the last value is returned.
        :param path: If it is empty, the top directory is used automatically.
        :return: All resulting values are Pandas dict output.
        """
        df = []
        if path:
            for entry in self.tree(rev=revision)[path]:
                df.append(self.__get_details(entry=entry, revision=revision))
        else:
            for entry in self.tree(rev=revision):
                df.append(self.__get_details(entry=entry, revision=revision))
        
        df = DataFrame(df)
        df["Name.Lower"] = df["name"].str.lower()
        df = df.sort_values(
            ["type2", "Name.Lower"],
            ignore_index=True,
            na_position='first'
        )
        df = df.drop(['Name.Lower', 'type2'], axis=1)
        df["id"] = df.index.map(lambda i: i + 1)
        data = df.to_dict(orient='records')
        del df
        return data
    
    def get_blob_details(
            self,
            revision: Union[str, Commit_ish, None] = None,
            path: str = None
    ) -> Dict:
        """
        It is for getting detailed information about any file.
        :param revision: If revision is left blank, the last value is returned.
        :param path: If it is empty, the top directory is used automatically.
        :return: Returns a Dict containing file data, name and size information
        """
        blob = self.tree(rev=revision)[path]
        data = blob.data_stream.read().decode()
        size = blob.data_stream.size
        return {
            'Data': data,
            'Size': size,
            'FileName': blob.name
        }
