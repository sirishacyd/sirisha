const axios = require('axios');

const GITHUB_USERNAME = 'your-github-username';
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;

const getRepos = async (username) => {
  let repos = [];
  let page = 1;
  while (true) {
    const url = `https://api.github.com/users/${username}/repos?per_page=100&page=${page}`;
    const response = await axios.get(url, {
      headers: {
        Authorization: `token ${GITHUB_TOKEN}`
      }
    });
    repos = repos.concat(response.data);
    if (response.data.length < 100) break;
    page++;
  }
  return repos;
};

const getCommitCount = async (repo) => {
  let commits = 0;
  let page = 1;
  while (true) {
    const url = `https://api.github.com/repos/${repo.full_name}/commits?per_page=100&page=${page}`;
    const response = await axios.get(url, {
      headers: {
        Authorization: `token ${GITHUB_TOKEN}`
      }
    });
    commits += response.data.length;
    if (response.data.length < 100) break;
    page++;
  }
  return commits;
};

const getTotalCommits = async (username) => {
  const repos = await getRepos(username);
  let totalCommits = 0;

  for (const repo of repos) {
    const commitCount = await getCommitCount(repo);
    totalCommits += commitCount;
  }

  return totalCommits;
};

(async () => {
  const totalCommits = await getTotalCommits(GITHUB_USERNAME);
  console.log(totalCommits);
})();
