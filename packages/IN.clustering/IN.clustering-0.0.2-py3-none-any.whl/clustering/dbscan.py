import numpy as np
from INClustering.utils import euclidean_distance

class DBSCAN:
    def __init__(self, epsilon, min_samples):
        self.epsilon = epsilon
        self.min_samples = min_samples

    def fit(self, X: np.ndarray):
        clustering = np.zeros(X.shape[0]) - 1
        _, core_point_indices = self.find_core_points(X)

        cluster_id = 0
        while core_point_indices.shape[0] > 0:
            new_cluster, used_core_points = self.form_cluster(X, core_point_indices)
            clustering[new_cluster] = cluster_id
            core_point_indices = np.delete(core_point_indices, used_core_points)
            cluster_id += 1
        return clustering

    def find_core_points(self, X: np.ndarray):

        """
        Finds the core points; that is, the points that have at least min_samples points neighboring them
        witing distance epsilon
        :param X: dataset
        :return: return all the core points in the dataset (core_points), and return boolean values stating where
        data point is core or not (helpful in indexing)
        """

        distances = euclidean_distance(X, X)
        # We care about points where distance is less that eplison, but greater than 0
        # (distance of 0 corresponds to the distance from the point to itself, which is the case for
        # all diagonal entries of the "distances" matrix
        reachibility_distance_within_epsilon = (distances < self.epsilon) & (distances > 0)
        reachibility_counts = np.count_nonzero(reachibility_distance_within_epsilon, axis=1)
        is_core_point = reachibility_counts >= self.min_samples
        core_points = X[is_core_point]

        core_point_indices = np.arange(X.shape[0])[is_core_point]
        return core_points, core_point_indices

    def form_cluster(self, X: np.ndarray, available_core_point_indices: np.ndarray):

        # choose a random core point

        # formed_cluster_indices = np.array([np.random.choice(available_core_point_indices)])
        random_choice_idx = np.random.choice(available_core_point_indices.shape[0])
        used_core_point_indices = np.array([random_choice_idx])
        formed_cluster_indices = np.array([available_core_point_indices[random_choice_idx]])
        # expand core points until convergence:
        while True:
            distances = euclidean_distance( X[ formed_cluster_indices ], X[available_core_point_indices] )
            # choose column indices that have distance less than eplison to formed_cluster indices
            is_core_point_reachable = (distances < self.epsilon) & (distances > 0)
            # find new pts: (points to be added)
            reachable_core_points = np.count_nonzero(is_core_point_reachable, axis=0) > 0
            new_core_point_indices = available_core_point_indices[reachable_core_points]
            used_core_point_indices = np.concatenate( (used_core_point_indices, np.arange(available_core_point_indices.shape[0])[reachable_core_points]) )
            size1 = formed_cluster_indices.shape[0]
            formed_cluster_indices = np.unique(np.concatenate((formed_cluster_indices, new_core_point_indices)))
            size2 = formed_cluster_indices.shape[0]
            # check if the core points have converged
            if size2 - size1 == 0:
                break

        # add non-core points:
        distances = euclidean_distance(X[formed_cluster_indices], X)
        reachable_non_core_points = (distances < self.epsilon) & (distances > 0)
        new_non_core_point_indices = np.arange(X.shape[0])[np.count_nonzero(reachable_non_core_points, axis=0) > 0]

        # TODO: POSSIBLE TO REMOVE UNIQUE?
        formed_cluster_indices = np.unique(np.concatenate((formed_cluster_indices, new_non_core_point_indices)))
        return formed_cluster_indices, used_core_point_indices